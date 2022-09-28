"""Open SQlite to get collections, books, and annotations.
"""

from glob import glob
import sqlite3
import os
from typing import Iterable
from core.models import Annotation, Book, Collection, Library


COLLECTION_QUERY = """
SELECT
	c.ZTITLE AS name,
	cb.ZCOLLECTION AS id,
	cb.ZASSETID AS book_id,
	b.ZAUTHOR AS author,
	b.ZTITLE AS book_title,
	COALESCE(ZDELETEDFLAG, 0) AS is_deleted
FROM
	ZBKCOLLECTIONMEMBER cb
LEFT JOIN ZBKCOLLECTION c ON
	cb.ZCOLLECTION = c.Z_PK
LEFT JOIN ZBKLIBRARYASSET b ON
	cb.ZASSETID = b.ZASSETID;
"""

BOOK_QUERY = """
SELECT
    ZASSETID AS id,
	ZAUTHOR AS author,
	ZTITLE AS title,
	ZGENRE AS genre,
	COALESCE(ZISNEW, 0) AS is_new,
	COALESCE(ZISFINISHED, 0) AS is_finished,
	DATETIME(ZDATEFINISHED + STRFTIME("%s", "2001-01-01"), "unixepoch") AS date_finished,
	DATETIME(ZCREATIONDATE + STRFTIME("%s", "2001-01-01"), "unixepoch") AS date_created,
	ROUND(ZREADINGPROGRESS * 100, 2) AS progress_percent,
	ZSORTAUTHOR AS sort_author,
	ZSORTTITLE AS sort_title
FROM
	ZBKLIBRARYASSET;
"""

ANNOTATION_QUERY = """
SELECT
	Z_PK AS id,
	ZANNOTATIONASSETID AS book_id,
	ZANNOTATIONSELECTEDTEXT AS selected_text,
	ZANNOTATIONNOTE AS note,
	ZANNOTATIONDELETED AS is_deleted,
	DATETIME(ZANNOTATIONCREATIONDATE + STRFTIME("%s", "2001-01-01"), "unixepoch") AS date_created
FROM
	ZAEANNOTATION
WHERE
	(ZANNOTATIONSELECTEDTEXT NOT NULL);
"""


def _dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return dict(zip(col_names, row))


def run_query(db: str, query: str) -> Iterable[dict]:
    """Run SQL query in SQLite"""
    con = sqlite3.connect(db)
    con.row_factory = _dict_factory
    for row in con.execute(query):
        yield row


class IBooksExtractor:
    """Extractor to get data about collections, books, and annotations from iBooks"""
    def __init__(
        self, book_path: str | None = None, annotation_path: str | None = None
    ):
        self._book_path = book_path
        self._annotation_path = annotation_path

    @property
    def book_path(self) -> str:
        """Generate book path from user input or as absolute path"""
        if self._book_path is not None:
            return self._book_path
        libpath = os.path.join(
            os.environ["HOME"],
            "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/",
        )
        return glob(os.path.join(libpath, "*.sqlite"))[0]

    @property
    def annotation_path(self) -> str:
        """Generate annotation path from user input or as absolute path"""
        if self._annotation_path is not None:
            return self._annotation_path
        libpath = os.path.join(
            os.environ["HOME"],
            "Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/",
        )
        return glob(os.path.join(libpath, "*.sqlite"))[0]

    def extract(self) -> Library:
        """Extract data"""
        annotations = [
            Annotation(**a) for a in run_query(self.annotation_path, ANNOTATION_QUERY)
        ]
        collections = [
            Collection(**c) for c in run_query(self.book_path, COLLECTION_QUERY)
        ]
        books = [Book(**b) for b in run_query(self.book_path, BOOK_QUERY)]
        for book in books:
            for collection in collections:
                if book.id == collection.book_id:
                    book.collections.append(collection.name)
            for annotation in annotations:
                if book.id == annotation.book_id:
                    book.annotations.append(annotation)
        return Library(books=books)


if __name__ == "__main__":
    test = IBooksExtractor()
    print(test.extract().json())
