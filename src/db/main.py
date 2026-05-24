from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text, SQLModel
from sqlalchemy.orm import sessionmaker
from src.config.config import settings

async_engine = create_async_engine(
    url=settings.async_database_url,
    echo=True
)

async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import Book, User
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS library"))
        await conn.run_sync(SQLModel.metadata.create_all)
        
    # Seed default user accounts if the users table is empty
    async_session = sessionmaker(
        bind=async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        from sqlmodel import select
        from src.db.models import User
        from src.auth_utils import hash_password
        
        statement = select(User)
        result = await session.exec(statement)
        if not result.first():
            print("Seeding default admin account...")
            admin_user = User(
                username="admin",
                hashed_password=hash_password("admin123"),
                role="admin"
            )
            session.add(admin_user)
            await session.commit()
            print("Default admin user seeded successfully!")

async def get_session() -> AsyncSession:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

