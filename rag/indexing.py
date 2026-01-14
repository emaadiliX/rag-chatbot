import os
import shutil
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from .ingestion import run_ingestion

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"


def get_embeddings():
    """
    Initialize the embedding model used for vectorizing document text.
    """
    return OpenAIEmbeddings(model="text-embedding-3-small")


def clear_chroma_db():
    """
    Remove the persisted ChromaDB directory if it exists.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def generate_chunk_id(chunk):
    """
    Generate a stable identifier for a document chunk based on its metadata.
    """
    source = chunk.metadata.get("source", "unknown_source")
    page = chunk.metadata.get("page", "unknown_page")
    chunk_id = chunk.metadata.get("chunk_id", "unknown_chunk")
    return f"{source}:{page}:{chunk_id}"


def load_chroma_db(embeddings):
    """
    Load or create a Chroma vector database with persistence enabled.
    """
    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )


def store_chunks(db, chunks, batch_size: int = 5000):
    """
    Add document chunks to the vector database.
    """
    ids = [generate_chunk_id(chunk) for chunk in chunks]

    for start in range(0, len(chunks), batch_size):
        end = start + batch_size
        db.add_documents(chunks[start:end], ids=ids[start:end])
        print(f"Stored chunks {start} -> {min(end, len(chunks))}")


def run_indexing(reset: bool = False):
    """
    Execute the indexing pipeline.

    The pipeline loads and chunks documents, generates embeddings,
    and stores the resulting vectors in a persistent Chroma database.
    """
    if reset:
        clear_chroma_db()

    chunks = run_ingestion("data/documents")

    embeddings = get_embeddings()
    db = load_chroma_db(embeddings)

    store_chunks(db, chunks)

    print(f"Indexed {len(chunks)} chunks successfully.")


if __name__ == "__main__":
    run_indexing(reset=True)
