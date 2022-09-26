"""Template for Book and Annotation classes.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class Annotation(BaseModel):
    """Annotation"""
    id: int
    selected_text: str
    note: str | None
    is_deleted: bool
    date_created: datetime  


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
    

class Collection(BaseModel):
    """Collection"""
    id: int
    name: str
    is_deleted: bool
    books: list[Book] = Field(default_factory=list)
    