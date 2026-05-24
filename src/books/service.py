from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select

class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self):
        statement = select(Book).order_by(Book.created_at)
        result = await self.session.exec(statement)
        return result.all()

    async def create_book(self, book_create_data: BookCreateModel):
        new_book = Book(**book_create_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def get_book(self, book_id: str):
        statement = select(Book).where(Book.uid == book_id)
        result = await self.session.exec(statement)
        return result.first()

    async def update_book(self, book_id: str, book_update_data: BookUpdateModel):
        statement = select(Book).where(Book.uid == book_id)
        result = await self.session.exec(statement)
        book = result.first()
        if not book:
            return None
        for key, value in book_update_data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def delete_book(self, book_id: str):
        statement = select(Book).where(Book.uid == book_id)
        result = await self.session.exec(statement)
        book = result.first()
        if not book:
            return None
        await self.session.delete(book)
        await self.session.commit()
        return True