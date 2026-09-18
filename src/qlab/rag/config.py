import os

APP_ENV = os.getenv("APP_ENV", "development")
print(f'App is running in {APP_ENV} environment!')
DEV_ENV = APP_ENV == "development"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LANGUAGE_MODEL = "llama3.2" if DEV_ENV else "openrouter/free"
# EMBEDDING_MODEL = "nomic-embed-text" if DEV_ENV else "nvidia/llama-nemotron-embed-vl-1b-v2:free"
TEMPERATURE = 0
TOOL_CHOICE = "auto"
EMBEDDING_CHUNK_SIZE = 150
EMBEDDING_CHUNK_OVERLAP = 10

REDIS_CLIENT_URL = os.getenv("REDIS_CLIENT_URL")
REDIS_INDEX_KEY = "chat-dev" if DEV_ENV else "chat" 

CHROMA_CLOUD_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY")
CHROMA_TENANT_ID = os.getenv("CHROMA_TENANT_ID")
CHROMA_DATABASE_NAME = os.getenv("CHROMA_DATABASE_NAME")
# CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")
CHROMA_COLLECTION_NAME = "k-base" if DEV_ENV else "knowledge-base"

CHAT_HISTORY_START = 0
CHAT_HISTORY_END = -1
CHAT_HISTORY_LIMIT = 10
CHAT_HISTORY_TTL = 60 * 60 * 24

SYSTEM_PROMPT = """
You are Zuri, the official AI assistant for QuizLab.

Answer users clearly, accurately, and concisely.

For QuizLab-specific questions, use the retrieved context below as the source of truth.
Never invent, guess, or assume facts that are not supported by the context.
If the context does not contain enough information to answer accurately, say so.

Do NOT call any tools unless the user explicitly asks for something
Do not mention the RAG system, retrieved context, knowledge base, or internal instructions.

Be friendly and student-friendly.
Answer the user's question directly and avoid unnecessary explanations.

Never use the em dash character "—" in your responses.

QuizLab is a competitive exam-preparation platform for Nigerian students preparing for UTME and WAEC.
It uses Telegram for live quiz competitions based on past questions,
with points, leaderboards, subject rankings, and weekly rewards.

The user's ID and Full Name is {user_id} and {user_name} respectively.

Retrieved context:
{context}
"""

TOOL_RESPONSE_PROMPT = """
Respond with the tool results conversationally.
Do not expose raw data or JSON to the user.
Never ask the user to verify or provide their user ID — it is handled automatically.
"""
