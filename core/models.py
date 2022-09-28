"""Template for Book and Annotation classes.
"""

from datetime import datetime
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

# pylint: disable=too-few-public-methods

class Annotation(BaseModel):
    """Annotation"""

    id: int
    selected_text: str
    note: str | None
    is_deleted: bool
    date_created: datetime
    book_id: str


class Collection(BaseModel):
    """Collection"""

    id: int
    name: str
    is_deleted: bool
    book_id: str


class Book(BaseModel):
    """Book"""

    id: str
    title: str
    author: str
    genre: str | None
    is_new: bool
    is_finished: bool
    date_created: datetime
    date_finished: datetime | None
    progress_percent: float
    sort_title: str
    sort_author: str
    annotations: list[Annotation] = Field(default_factory=list)
    collections: list[str] = Field(default_factory=list)


class Library(BaseModel):
    """Library"""

    books: list[Book]
