import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.main import get_session
from http import HTTPStatus
from .service import BookService
from .schemas import BookResponseModel, BookCreateModel, BookUpdateModel
from src.dependencies import require_admin
from src.db.models import User

book_router = APIRouter(prefix="/books")

def verify_uuid(book_id: str):
    try:
        uuid.UUID(book_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="The entered input is not of the standard UUID data type learn more about this in xyz.com"
        )

@book_router.get("/", response_model=List[BookResponseModel])
async def read_books(session: AsyncSession = Depends(get_session)):
    """
    Get all books
    """
    books = await BookService(session).get_all_books()
    return books

@book_router.post("/", response_model=BookResponseModel, status_code=HTTPStatus.CREATED)
async def create_book(
    book_create_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(require_admin)
):
    """
    Create a new book
    """
    new_book = await BookService(session).create_book(book_create_data)
    return new_book

@book_router.get("/{book_id}", response_model=BookResponseModel, status_code=HTTPStatus.OK)
async def read_book(book_id: str, session: AsyncSession = Depends(get_session)):
    """
    Get a book by ID
    """
    verify_uuid(book_id)
    book = await BookService(session).get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.put("/{book_id}", response_model=BookResponseModel, status_code=HTTPStatus.OK)
async def update_book(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(require_admin)
):
    """
    Update a book by ID
    """
    verify_uuid(book_id)
    updated_book = await BookService(session).update_book(book_id, book_update_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@book_router.delete("/{book_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(require_admin)
):
    """
    Delete a book by ID
    """
    verify_uuid(book_id)
    result = await BookService(session).delete_book(book_id)
    if result is False or result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {}
