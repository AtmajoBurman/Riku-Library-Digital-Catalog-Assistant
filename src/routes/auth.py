import os
import secrets
from datetime import timedelta
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth_utils import authenticate_user, create_access_token
from src.dependencies import get_current_user, require_admin
from src.auth_config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@auth_router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # If the user is already authenticated, redirect them straight to the admin dashboard.
    try:
        await require_admin(request, session)
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except Exception:
        pass
        
    # Generate a cryptographically secure random CSRF token
    csrf_token = secrets.token_hex(32)
    response = templates.TemplateResponse(request=request, name="login.html", context={"csrf_token": csrf_token})
    
    # Store CSRF token in an httpOnly cookie for double-submit verification
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=True,
        secure=False,  # Set to True in production with SSL
        samesite="lax"
    )
    return response

@auth_router.post("/login")
async def login(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    form_data = await request.form()
    form_csrf = form_data.get("csrf_token")
    cookie_csrf = request.cookies.get("csrf_token")
    
    # 1. CSRF Verification
    if not form_csrf or not cookie_csrf or form_csrf != cookie_csrf:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token validation failed. Possible Cross-Site Request Forgery attempt detected."
        )
        
    username = form_data.get("username")
    password = form_data.get("password")
    
    # 2. Authenticate User
    user = await authenticate_user(session, username, password)
    if not user or user.role != "admin":
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid username or password.", "csrf_token": cookie_csrf}
        )
        
    # 3. Create Access Token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # 4. Redirect using 303 (See Other) to convert POST to GET for admin dashboard
    response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    
    # Set the JWT in an httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with SSL
        samesite="lax"
    )
    # Clean up the login CSRF token cookie upon successful authentication
    response.delete_cookie("csrf_token")
    return response

@auth_router.get("/logout")
async def logout():
    # Redirect back to the frontend homepage using 303
    import os
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173/")
    response = RedirectResponse(url=frontend_url, status_code=status.HTTP_303_SEE_OTHER)
    # Invalidate session token by deleting cookie
    response.delete_cookie("access_token")
    return response
