# Riku: AI-Powered Digital Library Catalog Assistant

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97_Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

**Riku** is a modern, full-stack Library Management System integrated with an intelligent conversational assistant. It leverages natural language processing to empower library staff and members by providing an intuitive AI agent capable of querying the library database, finding books, and managing library operations through simple conversational prompts.

## 🚀 Key Features

- **AI-Powered Assistant (Riku):** Integrated Large Language Model (Llama-3.3-70B-Instruct) using LangChain's SQL Agent to naturally query the database. Users can ask questions like "Are there any books by J.K. Rowling available?" and Riku will directly query the DB and answer.
- **RESTful API Backend:** Built with FastAPI for high performance, utilizing asynchronous routes, automatic OpenAPI documentation, and Pydantic validation.
- **Modern Frontend:** React 19 web application built with Vite, ensuring a fast, responsive, and dynamic user interface.
- **Secure Authentication & Admin Portal:**
  - JWT-based authentication stored securely in `httpOnly` cookies.
  - Role-based access control (RBAC) protecting the Admin Dashboard.
  - Double-submit CSRF protection.
- **Robust Database Management:** PostgreSQL integration via `asyncpg` and `SQLModel` for reliable, type-safe database ORM and migrations.

## 🛠️ Tech Stack

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database & ORM:** PostgreSQL, [SQLModel](https://sqlmodel.tiangolo.com/), SQLAlchemy, asyncpg
- **AI & NLP:** [LangChain](https://langchain.com/), LangGraph, HuggingFace Hub (`meta-llama/Llama-3.3-70B-Instruct`)
- **Security:** bcrypt, python-jose (JWT), CSRF Protection

### Frontend
- **Framework:** [React 19](https://react.dev/)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **Tooling:** ESLint

## 📂 Directory Structure

```text
.
├── Makefile
├── README.md
├── requirements.txt
├── runserver.py
├── frontend/                 # React frontend application
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   └── src/                  # React components and pages
└── src/                      # FastAPI backend source code
    ├── __init__.py           # Application factory and routes
    ├── dependencies.py       # FastAPI dependencies
    ├── books/                # Book-related routes and logic
    ├── chatbot/              # LangChain AI agent integration
    │   └── code.py           # Core Llama 3 / Langchain implementation
    ├── config/               # App configuration
    ├── db/                   # Database models and session management
    │   ├── main.py           # DB connection
    │   └── models.py         # SQLModel schema definitions
    ├── routes/               # API endpoints
    │   ├── admin.py
    │   └── auth.py           # JWT and CSRF authentication logic
    └── templates/            # Jinja2 templates for auth/admin
```

---

## 🏗️ System Architecture

The application is structured into a separated frontend and backend architecture:

```mermaid
graph TD
    Client[React Frontend] -->|REST / JSON| API[FastAPI Backend]
    
    subgraph Backend Services
        API --> Auth[Auth & Admin Service]
        API --> BookSvc[Book Management Service]
        API --> Chatbot[AI Chatbot Endpoint]
        
        Chatbot -->|Natural Language| LangChain[LangChain SQL Agent]
        LangChain -->|Text Generation| HuggingFace[HuggingFace LLM]
        LangChain -->|Generated SQL| DB[(PostgreSQL Database)]
        
        Auth --> DB
        BookSvc --> DB
    end
```

### Flow of AI Interaction
1. **User Input:** The user submits a natural language question via the React frontend.
2. **Endpoint:** FastAPI receives the request at `/chatbot` and passes it to the LangChain executor.
3. **Reasoning:** The `Llama-3` model uses the `SQLDatabaseToolkit` to inspect the database schema.
4. **Execution:** The agent formulates a secure SQL query, executes it against the PostgreSQL database, and synthesizes a plain-English response.
5. **Response:** The text response is returned to the frontend.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL database
- Hugging Face API Token (for the Llama 3 model)

### 1. Clone the repository
```bash
git clone https://github.com/AtmajoBurman/Riku-Library-Digital-Catalog-Assistant.git
cd RESTAPI_project
```

### 2. Backend Environment Setup
Create a `.env` file in the project root with the following variables:
```env
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/library_db
SYNC_DATABASE_URL=postgresql://user:password@localhost:5432/library_db
ALLOWED_ORIGINS=http://localhost:5173
```
Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Frontend Environment Setup
Install Node.js dependencies:
```bash
make install
# This runs: npm install --prefix frontend
```

---

## 🏃‍♂️ Running the Application

A `Makefile` is provided for convenient process management.

To run both the FastAPI backend and the React frontend concurrently:
```bash
make run
```
*The backend will be available at `http://127.0.0.1:8000` (Swagger UI at `/docs`).*
*The frontend will be available at `http://127.0.0.1:5173`.*

**Other Makefile Commands:**
- `make run-backend`: Starts only the FastAPI server.
- `make run-frontend`: Starts only the Vite dev server.
- `make build`: Compiles the React frontend for production.

---

## 🔒 Security Posture
- **CSRF Tokens:** All sensitive form submissions (like login) require a cryptographically secure, double-submitted CSRF token.
- **Secure Cookies:** JWTs are stored in `httpOnly`, `samesite=lax` cookies to mitigate XSS and CSRF attacks.
- **SQL Injection Prevention:** Parameterized queries via SQLModel and secure bounds around the LangChain SQL Agent.

---

## 👨‍💻 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.
