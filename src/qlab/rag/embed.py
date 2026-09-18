from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from openai import OpenAI
from .config import APP_ENV, OPENROUTER_API_KEY

class OpenRouterEmbeddings(Embeddings):
    def __init__(self, model: str, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            encoding_format="float",
        )

        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            encoding_format="float",
        )

        return response.data[0].embedding

def get_embedding_model():
    embedding_model = None

    match APP_ENV:
        case 'production':
            embedding_model = OpenRouterEmbeddings(model="nvidia/llama-nemotron-embed-vl-1b-v2:free", api_key=OPENROUTER_API_KEY)
        case 'development':
            embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    return embedding_model

embeddings = get_embedding_model()