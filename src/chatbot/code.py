# =============================================================================
# Imports
# =============================================================================
from src.chatbot.demonstration import DEMONSTRATION_VIDEO
from sqlalchemy import create_engine, text, inspect
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
from src.chatbot.helper_transform_pg_url import transform_pg_url
from src.chatbot.model_name import MODEL_NAME
from src.chatbot.system_prompt import SYSTEM_PROMPT

# =============================================================================
# Environment
# =============================================================================
DATABASE_URL = os.getenv("POSTGRES_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = transform_pg_url(DATABASE_URL)

# =============================================================================
# Database connection (SQLAlchemy only)
# =============================================================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

# =============================================================================
# SCHEMA = <Name>
# =============================================================================
SCHEMA = "library" 

# =============================================================================
# Helper: get schema + sample rows (replaces sample_rows_in_table_info)
# =============================================================================
def get_table_info(table_names: list[str] | None = None, sample_rows: int = 3) -> str:
    insp = inspect(engine)
    tables = table_names or insp.get_table_names(schema=SCHEMA)
    parts = []

    with engine.connect() as conn:
        for table in tables:
            cols = insp.get_columns(table, schema=SCHEMA)
            col_defs = ", ".join(f"{c['name']} {c['type']}" for c in cols)
            parts.append(f"Table: {SCHEMA}.{table}\nColumns: {col_defs}")

            try:
                result = conn.execute(
                    text(f'SELECT * FROM "{SCHEMA}"."{table}" LIMIT {sample_rows}')
                )
                rows = result.fetchall()
                if rows:
                    col_names = list(result.keys())
                    sample = "\n".join("\t".join(str(v) for v in row) for row in rows)
                    parts.append(
                        f"/* {sample_rows} sample rows:\n"
                        + "\t".join(col_names) + "\n" + sample + "\n*/"
                    )
            except Exception as e:
                parts.append(f"(Could not fetch sample rows: {e})")
            parts.append("")
    return "\n".join(parts)

# =============================================================================
# Tools (modern @tool style)
# =============================================================================
@tool
def list_tables() -> str:
    """Return a comma-separated list of all table names in the database."""
    insp = inspect(engine)
    tables = insp.get_table_names(schema=SCHEMA)
    return ", ".join(tables)

@tool
def get_schema(table_names: str) -> str:
    """Input is a comma-separated list of table names.
    Returns schema + a few sample rows for each table.
    Always call list_tables first to know which tables exist."""
    names = [t.strip() for t in table_names.split(",") if t.strip()]
    return get_table_info(names, sample_rows=3)

@tool
def execute_sql(query: str) -> str:
    """Execute a READ-ONLY SQL query and return the results.
    Only SELECT / WITH queries are allowed."""
    cleaned = query.strip().lower()
    if not (cleaned.startswith("select") or cleaned.startswith("with")):
        return "ERROR: Only SELECT or WITH queries are allowed."

    try:
        with engine.connect() as conn:
            # Make sure the search_path includes the library schema
            conn.execute(text(f'SET search_path TO "{SCHEMA}", public'))
            result = conn.execute(text(query))
            rows = result.fetchall()
            return str(rows[:50]) if rows else "No rows returned."
    except Exception as e:
        return f"Error executing query: {e}"

tools = [list_tables, get_schema, execute_sql]

# =============================================================================
# LLM
# =============================================================================
llm = ChatGroq(
    model=MODEL_NAME,
    temperature=1,
)

# =============================================================================
# Create the modern agent
# =============================================================================
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

# =============================================================================
# Ask the agent
# =============================================================================
def ask(question: str):
    """Ask a natural language question to the SQL agent."""
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    # The final answer is the last message from the agent
    return result["messages"][-1].content

# =============================================================================
# Get chatbot response
# =============================================================================
def get_chatbot_response(user_input: str) -> str:
    """
    Chatbot temporarily disabled.
    Returns a maintenance message instead of invoking the LLM.
    """

    link = DEMONSTRATION_VIDEO  # Replace with your actual demo/video URL
    try:
        return ask(user_input)
    except Exception as e:
        print("Error from SQL agent:", e)
        return (
            "It seems we have run into a problem, we are trying to fix this and we apologize for the inconvenience. "
            f"In the meantime, you can view this: <a href='{link}' target='_blank' style='color: blue; text-decoration: none;'>Demonstration Video</a> to understand how this Library Management System actually works. "
            "Thank you for your patience."
        )
