from demonstration import DEMONSTRATION_VIDEO
# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# import os
# import logging
# from dotenv import load_dotenv
# from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
# from langchain_community.utilities import SQLDatabase
# from langchain_community.agent_toolkits import create_sql_agent
# from langchain_classic.memory import ConversationBufferMemory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# import re


# def strip_markdown(text):
#     # Remove bold/italic markers
#     text = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', text)
#     # Remove headings (#)
#     text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
#     return text

# # Set up logging
# logger = logging.getLogger(__name__)

# load_dotenv()

# _agent_executor = None

# def build_agent_executor(model_repo_id: str):
#     from src.config.config import settings
#     hf_api_ = os.getenv("HUGGINGFACEHUB_API_TOKEN", "").strip()
#     db_url = settings.sync_database_url

#     if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
#         db = SQLDatabase.from_uri(db_url, schema="library")
#     else:
#         db = SQLDatabase.from_uri(db_url)

#     llm_endpoint = HuggingFaceEndpoint(
#         repo_id=model_repo_id,
#         huggingfacehub_api_token=hf_api_,
#         provider="together",
#         stop_sequences=["\nObservation:", "Observation:"],
#         temperature=0.1
#     )
#     llm = ChatHuggingFace(llm=llm_endpoint)

#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         return_messages=False
#     )

#     SYSTEM_PREFIX = """
# You are a helpful assistant working for a library management software.
# Your name is Riku.
# You help library staff and members with queries about books, members, 
# borrowing history, fines, and availability.

# If the user asks something related to the library database, query it and answer.
# If the user asks a general question or greets you, respond conversationally 
# and politely without querying the database.
# If the user asks something completely outside the library domain, 
# politely say it is outside your scope.

# CRITICAL INSTRUCTION:
# When using a tool, output only:
# Action: <tool_name>
# Action Input: <input>
# Do not write "Observation:" or simulate results.

# When giving your final answer, output:
# Final Answer: <your response>

# NOTE: Answer briefly and to the point. Format your response in plain ENGLISH TEXT without markdown.
# """

#     toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#     from langchain_core.prompts import PromptTemplate
#     from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_SUFFIX
#     from langchain_classic.agents.mrkl.prompt import FORMAT_INSTRUCTIONS

#     template = "\n\n".join([
#         SYSTEM_PREFIX,
#         SQL_PREFIX,
#         "{tools}",
#         FORMAT_INSTRUCTIONS,
#         "Previous Conversation:\n{chat_history}",
#         SQL_SUFFIX
#     ])

#     prompt = PromptTemplate.from_template(template)
#     prompt = prompt.partial(dialect=toolkit.dialect, top_k="10")

#     return create_sql_agent(
#         llm=llm,
#         toolkit=toolkit,
#         agent_type="zero-shot-react-description",
#         verbose=True,
#         prompt=prompt,
#         max_iterations=5,
#         agent_executor_kwargs={
#             "handle_parsing_errors": True,
#             "handle_tool_error": True,
#             "memory": memory
#         }
#     )

# def get_agent_executor(model_name: str = "meta-llama/Llama-3.3-70B-Instruct"):
#     global _agent_executor
#     if _agent_executor is None:
#         try:
#             _agent_executor = build_agent_executor(model_name)
#         except Exception as e:
#             logger.error(f"Error initializing chatbot agent executor with {model_name}: {e}", exc_info=True)
#             raise e
#     return _agent_executor

def get_chatbot_response(user_input: str) -> str:
    """
    Chatbot temporarily disabled.
    Returns a maintenance message instead of invoking the LLM.
    """

    link = DEMONSTRATION_VIDEO  # Replace with your actual demo/video URL

    return (
        "This feature is currently under maintenance. Visitors are requested to bear with us. "
        f"You are requested to view this: <a href='{link}' target='_blank' style='color: blue; text-decoration: none;'>Demonstration Video</a> to understand how this Library Management System actually works. "
        "Thank you for your patience."
    )
#     """
#     Invokes the chatbot agent with the given user input and returns the generated text response.
#     Falls back to secondary model if primary model hits credit limits or HTTP errors.
#     """
#     primary_model = "meta-llama/Llama-3.3-70B-Instruct"
#     fallback_model = "Qwen/Qwen2.5-Coder-32B-Instruct"

#     try:
#         agent = get_agent_executor(primary_model)
#         response = agent.invoke({"input": user_input})
#         return strip_markdown(response.get("output", "No response generated."))
#     except Exception as e:
#         logger.warning(f"Primary model ({primary_model}) failed: {e}. Trying fallback model ({fallback_model})...")
#         try:
#             fallback_agent = build_agent_executor(fallback_model)
#             response = fallback_agent.invoke({"input": user_input})
#             return strip_markdown(response.get("output", "No response generated."))
#         except Exception as fallback_err:
#             logger.error(f"Fallback model also failed: {fallback_err}", exc_info=True)
#             return "I encountered an error while processing your request. Please try again later."