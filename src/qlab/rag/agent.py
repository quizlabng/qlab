from langchain_openrouter import ChatOpenRouter
from langchain_ollama import ChatOllama

from .config import APP_ENV, OPENROUTER_API_KEY, TOOL_CHOICE
from .tools import tools

def get_language_model():
    language_model = None

    match APP_ENV:
        case 'production':
            language_model = ChatOpenRouter(model="openrouter/free", api_key=OPENROUTER_API_KEY)
        case 'development':
            language_model = ChatOllama(model="granite4.1:3b")

    return language_model

llm = get_language_model()
agent = llm.bind_tools(tools=tools, tool_choice=TOOL_CHOICE)