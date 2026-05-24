from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
import logging
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import re


def strip_markdown(text):
    # Remove bold/italic markers
    text = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', text)
    # Remove headings (#)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    return text

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

_agent_executor = None

def get_agent_executor():
    global _agent_executor
    if _agent_executor is None:
        try:
            from src.config.config import settings
            hf_api_ = os.getenv("HUGGINGFACEHUB_API_TOKEN")
            db_url = settings.sync_database_url

            # Conditionally pass schema only for PostgreSQL
            if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
                db = SQLDatabase.from_uri(db_url, schema="library")
            else:
                db = SQLDatabase.from_uri(db_url)

            llm_endpoint = HuggingFaceEndpoint(
                repo_id="meta-llama/Llama-3.3-70B-Instruct",
                huggingfacehub_api_token=hf_api_
            )
            llm = ChatHuggingFace(llm=llm_endpoint)

            memory = ConversationBufferMemory(
                memory_key="chat_history",      # key must match agent_kwargs input_variables
                return_messages=True
            )

            SYSTEM_PREFIX = """
You are a helpful assistant working for a library management software.
Your name is Riku.
You help library staff and members with queries about books, members, 
borrowing history, fines, and availability.

If the user asks something related to the library database, query it and answer.
If the user asks a general question or greets you, respond conversationally 
and politely without querying the database.
If the user asks something completely outside the library domain, 
politely say it is outside your scope.

NOTE: Answer briefly and to the point. DO NOT speak excessively. Format you response in plain ENGLISH TEXT without markdown.
"""

            toolkit = SQLDatabaseToolkit(db=db, llm=llm)

            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PREFIX),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            _agent_executor = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                agent_type="tool-calling",
                verbose=True,
                prompt=prompt,
                agent_executor_kwargs={
                    "handle_parsing_errors": True,
                    "handle_tool_error": True,
                    "memory": memory
                }
            )
        except Exception as e:
            logger.error(f"Error initializing chatbot agent executor: {e}", exc_info=True)
            raise e
            
    return _agent_executor

def get_chatbot_response(user_input: str) -> str:
    """
    Invokes the chatbot agent with the given user input and returns the generated text response.
    """
    try:
        agent = get_agent_executor()
        response = agent.invoke({"input": user_input})
        return strip_markdown(response.get("output", "No response generated."))
    except Exception as e:
        logger.error(f"Error invoking chatbot agent: {e}", exc_info=True)
        # tODO(security): Return a safe, generic message to the user rather than raw traces
        return "I encountered an error while processing your request. Please try again later."