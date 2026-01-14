import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from ingestion import run_ingestion

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"
DATA_DIR = "data/documents"


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print(f"Cleared existing database")


def create_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


def get_chunk_id(chunk):
    source = chunk.metadata.get("source", "unknown")
    page = chunk.metadata.get("page", 0)
    chunk_num = chunk.metadata.get("chunk_id", 0)
    return f"{source}:p{page}:c{chunk_num}"


def index_documents(reset=False):
    if reset:
        clear_database()

    # Load and chunk documents
    print("Loading documents...")
    chunks = run_ingestion(DATA_DIR)
    print(f"Got {len(chunks)} chunks")

    # Create embeddings
    print("Creating embeddings...")
    embeddings = create_embeddings()

    # Create vector store
    print("Building vector database...")
    chunk_ids = [get_chunk_id(chunk) for chunk in chunks]

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=chunk_ids,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )

    print(f"Indexed {len(chunks)} chunks successfully")
    return db


if __name__ == "__main__":
    index_documents(reset=True)
