import redis
import json

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, ToolMessage
from .config import REDIS_CLIENT_URL, REDIS_INDEX_KEY, CHAT_HISTORY_START, CHAT_HISTORY_END, CHAT_HISTORY_LIMIT
from .ingest import vectore_store

retriever = vectore_store.as_retriever()
redis_client = redis.from_url(url=REDIS_CLIENT_URL)

def get_relevant_context(query: str) -> str:
    retrived_docs = retriever.invoke(query)
    relevant_context = "\n".join([doc.page_content for doc in retrived_docs])
    return relevant_context


def get_user_chat_history(user_id: str) -> list[BaseMessage]:
    chat_history = []
    conversations = redis_client.lrange(f'{REDIS_INDEX_KEY}:{user_id}', CHAT_HISTORY_START, CHAT_HISTORY_END)
    
    for conversation in reversed(conversations):
        for message in json.loads(conversation):
            message_role, message_content = message['role'], message['content']
            match message_role:
                case 'system':
                    chat_history.append(SystemMessage(content=message_content))
                case 'human':
                    chat_history.append(HumanMessage(content=message_content))
                case 'ai':
                    chat_history.append(AIMessage(content=message_content))
                case 'tool':
                    chat_history.append(ToolMessage(content=message_content, tool_call_id=message['id']))
                case _:
                    chat_history.append(BaseMessage(content=message_content))

    return chat_history

def save_user_chat_messages(user_id: int, messages: list[dict]) -> None:
    redis_client.lpush(f'{REDIS_INDEX_KEY}:{user_id}', json.dumps(messages))
    redis_client.ltrim(f'{REDIS_INDEX_KEY}:{user_id}', CHAT_HISTORY_START, CHAT_HISTORY_LIMIT - 1)