import os
import shutil
import time
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from .ingestion import run_ingestion

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"
DATA_DIR = "data/documents"
BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "500"))


def _db_exists():
    return (
        os.path.isdir(CHROMA_PATH)
        and os.path.exists(os.path.join(CHROMA_PATH, "chroma.sqlite3"))
    )


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Cleared existing database")


def create_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        chunk_size=BATCH_SIZE,
        max_retries=3,
        show_progress_bar=True,
    )


def get_chunk_id(chunk):
    source = chunk.metadata.get("source", "unknown")
    page = chunk.metadata.get("page", 0)
    chunk_num = chunk.metadata.get("chunk_id", 0)
    return f"{source}:p{page}:c{chunk_num}"


def index_documents(reset=False):
    start_total = time.time()

    if not reset and _db_exists():
        print("Vector database already exists. Skipping indexing.")
        print("Run with reset=True to rebuild.")
        return None

    if reset:
        clear_database()

    print("Loading and chunking documents...")
    chunks = run_ingestion(DATA_DIR)
    total_chunks = len(chunks)

    print(f"Creating embeddings for {total_chunks} chunks (batch size: {BATCH_SIZE})...")

    embeddings = create_embeddings()
    chunk_ids = [get_chunk_id(chunk) for chunk in chunks]

    db = None
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_end = min(i + BATCH_SIZE, total_chunks)
        batch_chunks = chunks[i:batch_end]
        batch_ids = chunk_ids[i:batch_end]

        progress = (batch_end / total_chunks) * 100
        print(f"Processing batch {i // BATCH_SIZE + 1}: chunks {i + 1}-{batch_end} ({progress:.1f}%)")

        if db is None:
            db = Chroma.from_documents(
                documents=batch_chunks,
                embedding=embeddings,
                ids=batch_ids,
                persist_directory=CHROMA_PATH,
                collection_name=COLLECTION_NAME,
            )
        else:
            db.add_documents(documents=batch_chunks, ids=batch_ids)

    total_time = time.time() - start_total
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)

    print(f"Indexing complete. {total_chunks} chunks indexed in {minutes}m {seconds}s.")
    return db


if __name__ == "__main__":
    index_documents(reset=True)
