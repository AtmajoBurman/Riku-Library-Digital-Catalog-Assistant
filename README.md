# Riku: AI-Powered Digital Library Catalog Assistant

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)

**Riku** is an enterprise-grade Library Management System equipped with an intelligent conversational assistant. By bridging state-of-the-art Large Language Models with a robust RESTful architecture, Riku enables library staff and patrons to query the catalog, discover books, and manage operations through intuitive natural language interactions.

## 🚀 Key Features

- **AI-Powered Natural Language Interface:** Utilizes LangChain and the Llama-3.3-70B-Instruct model to translate conversational prompts into precise, secure SQL queries.
- **High-Performance REST API:** Built on FastAPI with asynchronous endpoints, comprehensive Pydantic validation, and automated OpenAPI documentation.
- **Modern React Web Application:** A responsive and dynamic frontend built with React 19 and Vite.
- **Industry-Standard Security:** Features double-submit CSRF protection, secure `httpOnly` JWT session management, and granular Role-Based Access Control (RBAC).
- **Comprehensive Observability:** Integrated telemetry using Prometheus for metrics scraping and Grafana for real-time performance visualization, all orchestrated via Docker.

## 🛠️ Tech Stack

### Application Layer
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Frontend:** [React 19](https://react.dev/), [Vite](https://vitejs.dev/)
- **Database & ORM:** PostgreSQL, [SQLModel](https://sqlmodel.tiangolo.com/), SQLAlchemy, asyncpg
- **AI & NLP:** [LangChain](https://langchain.com/), LangGraph, HuggingFace Hub (`meta-llama/Llama-3.3-70B-Instruct`)
- **Security:** bcrypt, python-jose (JWT)

### Infrastructure & Observability
- **Containerization:** **Docker** and **Docker Compose** isolate and manage the lifecycle of infrastructure services, ensuring environment consistency across development and production.
- **Metrics Collection:** **Prometheus** periodically scrapes the backend's `/metrics` endpoint to collect time-series data such as HTTP request counts, system latency, and resource utilization.
- **Data Visualization:** **Grafana** connects to Prometheus to provide highly customizable, real-time interactive dashboards that offer deep insights into system health and API performance.

## 📂 Directory Structure

```text
.
├── docker-compose.yml        # Orchestrates the observability stack (Prometheus & Grafana)
├── Makefile                  # Developer shortcuts for building and running the application
├── prometheus.yml            # Configuration for Prometheus metrics scraping
├── frontend/                 # React SPA
│   ├── src/                  # React components and views
│   └── vite.config.js
├── grafana/                  # Pre-configured Grafana datasources and dashboards
└── src/                      # FastAPI backend
    ├── __init__.py           # Application factory and route registration
    ├── books/                # Book inventory management
    ├── chatbot/              # LangChain orchestration (Llama 3)
    ├── db/                   # Database models and async session management
    ├── metrics.py            # Prometheus metrics middleware and export handlers
    └── routes/               # API endpoints (auth, admin, metrics)
```

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client[React Frontend] -->|REST / JSON| API[FastAPI Backend]
    
    subgraph Core Services
        API --> Auth[Auth & Admin]
        API --> BookSvc[Book Management]
        API --> Chatbot[AI Chatbot Endpoint]
        
        Chatbot -->|Natural Language| LangChain[LangChain SQL Agent]
        LangChain -->|Generated SQL| DB[(PostgreSQL Database)]
        
        Auth --> DB
        BookSvc --> DB
    end

    subgraph Observability Stack
        Prometheus[Prometheus] -->|Scrapes /metrics| API
        Grafana[Grafana Dashboard] -->|Queries| Prometheus
    end
```

### AI Workflow
1. User submits a natural language question via the React UI.
2. The `/chatbot` endpoint passes the request to the LangChain executor.
3. The model inspects the database schema and formulates a secure SQL query.
4. The database executes the query, and the LLM synthesizes a plain-English response.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- PostgreSQL database
- Docker & Docker Compose (for the observability stack)
- Hugging Face API Token (for the Llama 3 model)

### 1. Environment Configuration

Clone the repository and set up your `.env` file in the project root:

```env
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/library_db
SYNC_DATABASE_URL=postgresql://user:password@localhost:5432/library_db
ALLOWED_ORIGINS=http://localhost:5173
```

### 2. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
make install
```

---

## 🏃‍♂️ Running the Application

### 1. Start the Core Application
Start both the FastAPI backend and the React frontend concurrently using the provided Makefile:
```bash
make run
```
- Backend (API & Swagger Docs): `http://127.0.0.1:8000`
- Frontend UI: `http://127.0.0.1:5173`

*(Alternatively, use `make run-backend` and `make run-frontend` to start them in separate terminal sessions).*

### 2. Launch the Observability Stack (Docker)
To monitor API metrics and system health, spin up the Prometheus and Grafana containers:
```bash
docker compose up -d
```
- **Access Grafana:** Navigate to `http://localhost:3000` (Default login: `admin` / `admin`).
- A pre-configured **FastAPI Metrics** dashboard is automatically provisioned and ready for use.

---

## 🔒 Security Posture
- **CSRF Protection:** State-changing requests enforce cryptographically secure, double-submitted CSRF tokens.
- **Secure Sessions:** Authentication is maintained via JWTs stored in `httpOnly`, `SameSite=Lax` cookies, neutralizing XSS vector attacks.
- **SQL Injection Prevention:** Enforced parameterized queries via SQLModel and stringent validation boundaries around the LangChain SQL Agent.

---

## 👨‍💻 Contributing
Pull requests are welcome. For major architectural changes or feature additions, please open an issue first to discuss the proposed updates. Ensure you update tests as appropriate.
