from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from src.config.version import API_VERSION
from src.db.main import init_db
from src.books.routes import book_router
from src.routes.auth import auth_router
from src.routes.admin import admin_router
from pydantic import BaseModel
from src.chatbot.code import get_chatbot_response
from src.metrics import PrometheusMiddleware, metrics_handler

from contextlib import asynccontextmanager

# the work of asynccontextmanager is to manage the lifespan of the application
#  can run code at the startup and shutdown of the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    print("Server Starting Up")
    await init_db()
    yield
    #shutdown
    print("Server Shutting Down")

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = 'Book service',
    version = API_VERSION,
    description = 'A simple book service API',
    lifespan = lifespan
)

# Configure CORS
import os
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)

app.include_router(book_router, tags=["Books"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(admin_router, tags=["Admin Portal"])

app.add_api_route("/metrics", metrics_handler, methods=["GET"], tags=["Metrics"])

@app.get("/")
async def index():
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/health")
async def health_check():
    return {
            'status': 'ok', 
            'version':API_VERSION,
            # 'database_connected':is_database_connected()
            }

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chatbot", response_model=ChatResponse, tags=["Chatbot"])
async def chat_with_assistant(request: ChatRequest):
    """
    Interact with Riku, the library assistant.
    """
    try:
        response_text = get_chatbot_response(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        # tODO(security): Return a safe, generic error message and log the traceback internally
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your query with the assistant."
        )

