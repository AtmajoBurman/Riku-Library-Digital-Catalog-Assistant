from fastapi import Request, HTTPException, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.db.models import User
from src.auth_utils import decode_token
from typing import Optional

async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.first()

async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing. Please log in."
        )
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or token is invalid. Please log in again."
        )
        
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is invalid. Please log in again."
        )
        
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user no longer exists."
        )
        
    return user

async def require_admin(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    user = await get_current_user(request, session)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required to access this resource."
        )
    return user
