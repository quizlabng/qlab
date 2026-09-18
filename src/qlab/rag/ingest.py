import os
from glob import glob

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from .embed import embeddings

from .config import EMBEDDING_CHUNK_SIZE, EMBEDDING_CHUNK_OVERLAP, CHROMA_CLOUD_API_KEY, CHROMA_TENANT_ID, CHROMA_DATABASE_NAME, CHROMA_COLLECTION_NAME

vectore_store = Chroma(
    chroma_cloud_api_key=CHROMA_CLOUD_API_KEY,
    tenant=CHROMA_TENANT_ID,
    database=CHROMA_DATABASE_NAME,
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=embeddings,
    create_collection_if_not_exists=True,
)


def seed_knowledge_base() -> None:
    knowledge_base_dir = "knowledge-base"
    if not os.path.exists(knowledge_base_dir):
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=EMBEDDING_CHUNK_SIZE, chunk_overlap=EMBEDDING_CHUNK_OVERLAP)

    txt_files = glob(os.path.join(knowledge_base_dir, "*.txt"))
    for file_path in txt_files:
        loader = TextLoader(
            file_path=file_path,
            encoding="utf-8"
        )
        documents = loader.load_and_split(text_splitter=text_splitter)
        vectore_store.add_documents(documents=documents)

if __name__ == "__main__":
    seed_knowledge_base()