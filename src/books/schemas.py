from src.db.models import Book
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    isbn: str
    description: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "description": "A novel set in the Roaring Twenties, exploring themes of wealth"
            }
        }
    }

class BookResponseModel(BaseModel):
    uid: UUID
    title: str  
    author: str
    isbn: str
    description: str
    is_available: bool
    created_at: datetime
    updated_at: datetime
    model_config = {
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "description": "A novel set in the Roaring Twenties, exploring themes of wealth",
                "is_available": True,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
    }       

from typing import Optional

class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None

class Query(BaseModel):
    query: str

