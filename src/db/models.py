from sqlmodel import SQLModel, Field
from uuid import UUID
from sqlalchemy import Column, String
from uuid import uuid4
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime as dt


class Book(SQLModel, table =True):
    __tablename__ = "books"

    uid: UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, index=True)
    )
    title: str = Field(max_length=120, default="", index=True)
    author: str = Field(max_length=120, default="", index=True)
    isbn: str = Field(max_length=120, default="", index=True)
    description: str = Field(default="")
    is_available: bool = Field(default=True)
    created_at: dt = Field(default_factory=dt.now)
    updated_at: dt = Field(default_factory=dt.now, sa_column_kwargs={"onupdate": dt.now})
    
    __table_args__ = {"schema": "library"}

    def __repr__(self): 
        return f"Book(uid={self.uid}, title='{self.title}', author='{self.author}', isbn='{self.isbn}', is_available={self.is_available})"


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False, index=True)
    )
    username: str = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    hashed_password: str = Field(nullable=False)
    role: str = Field(default="user", max_length=20)
    created_at: dt = Field(default_factory=dt.now)

    __table_args__ = {"schema": "library"}

    def __repr__(self):
        return f"User(uid={self.uid}, username='{self.username}', role='{self.role}')"
