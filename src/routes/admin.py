import os
from fastapi import APIRouter, Request, Depends, HTTPException, status
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.dependencies import get_current_user, require_admin
from sqlmodel import select
from src.db.models import Book

admin_router = APIRouter(prefix="/admin")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@admin_router.get("", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    try:
        current_user = await require_admin(request, session)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        return templates.TemplateResponse(
            request=request,
            name="403.html",
            context={"user": getattr(e, "user", None), "frontend_url": frontend_url},
            status_code=status.HTTP_403_FORBIDDEN
        )
        
    # Fetch books list to display on admin dashboard
    statement = select(Book).order_by(Book.created_at)
    result = await session.exec(statement)
    books = result.all()
    
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"user": current_user, "books": books, "frontend_url": frontend_url}
    )

@admin_router.get("/secret", response_class=HTMLResponse)
async def admin_secret(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    try:
        current_user = await require_admin(request, session)
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        # Render a custom 403 template if forbidden
        return templates.TemplateResponse(
            request=request,
            name="403.html",
            context={"user": getattr(e, "user", None), "frontend_url": frontend_url},
            status_code=status.HTTP_403_FORBIDDEN
        )
        
    return templates.TemplateResponse(
        request=request,
        name="admin_secret.html",
        context={"user": current_user, "frontend_url": frontend_url}
    )

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

@admin_router.post("/change-password")
async def change_password(
    data: ChangePasswordRequest,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    current_user = await require_admin(request, session)
    
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New passwords do not match."
        )
        
    from src.auth_utils import hash_password
    current_user.hashed_password = hash_password(data.new_password)
    session.add(current_user)
    await session.commit()
    
    return {"status": "success", "message": "Password updated successfully."}
