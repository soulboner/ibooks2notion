"""Open SQlite to get collections, books, and annotations.
"""

import sqlite3


COLLECTION_QUERY = """ 
SELECT
	c.ZTITLE AS collection,
	cb.ZCOLLECTION AS collection_id,
	cb.ZASSETID AS book_asset_id,
	b.ZAUTHOR AS author,
	b.ZTITLE AS book_title,
	COALESCE(ZDELETEDFLAG, 0) AS is_collection_deleted
FROM
	ZBKCOLLECTIONMEMBER cb
LEFT JOIN ZBKCOLLECTION c ON
	cb.ZCOLLECTION = c.Z_PK
LEFT JOIN ZBKLIBRARYASSET b ON
	cb.ZASSETID = b.ZASSETID;
"""

BOOK_QUERY = """ 
SELECT
	ZAUTHOR AS author,
	ZTITLE AS book_title,
	ZGENRE AS book_genre,
	COALESCE(ZISNEW, 0) AS is_new,
	COALESCE(ZISFINISHED, 0) AS is_finished,
	DATETIME(ZDATEFINISHED + STRFTIME("%s", "2001-01-01"), "unixepoch") AS date_finished,
	DATETIME(ZCREATIONDATE + STRFTIME("%s", "2001-01-01"), "unixepoch") AS date_created,
	ROUND(ZREADINGPROGRESS * 100, 2) AS progress_percent,
	ZASSETID AS book_asset_id,
	ZASSETGUID AS book_asset_guid,
	ZSORTAUTHOR AS sort_author,
	ZSORTTITLE AS book_sort_title
FROM
	ZBKLIBRARYASSET;
"""

ANNOTATION_QUERY = """ 
SELECT
	Z_PK AS annotation_id,
	ZANNOTATIONASSETID AS book_asset_id,
	ZANNOTATIONSELECTEDTEXT AS SELECTed_text,
	ZANNOTATIONNOTE AS annotation_note,
	ZANNOTATIONDELETED AS is_annotation_deleted,
	DATETIME(ZANNOTATIONCREATIONDATE + STRFTIME("%s", "2001-01-01"), "unixepoch") AS annotation_date_created
FROM
	ZAEANNOTATION
where
	(ZANNOTATIONSELECTEDTEXT NOT NULL);
"""
