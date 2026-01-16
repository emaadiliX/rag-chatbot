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
BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "1000"))


def db_exists():
    return (
        os.path.isdir(CHROMA_PATH)
        and os.path.exists(os.path.join(CHROMA_PATH, "chroma.sqlite3"))
    )


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Cleared existing database")


def get_chunk_id(chunk):
    source = chunk.metadata.get("source", "unknown")
    page = chunk.metadata.get("page", 0)
    chunk_num = chunk.metadata.get("chunk_id", 0)
    return f"{source}:p{page}:c{chunk_num}"


def index_documents(reset=False):
    start_time = time.time()

    if not reset and db_exists():
        print("Vector database already exists. Skipping indexing.")
        print("Run with reset=True to rebuild.")
        return None

    if reset:
        clear_database()

    print("Loading and chunking documents...")
    chunks = run_ingestion(DATA_DIR)
    total = len(chunks)

    print(f"Indexing {total} chunks (batch size: {BATCH_SIZE})...")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        chunk_size=BATCH_SIZE,
    )

    chunk_ids = [get_chunk_id(c) for c in chunks]

    db = None
    for i in range(0, total, BATCH_SIZE):
        batch_end = min(i + BATCH_SIZE, total)
        batch_chunks = chunks[i:batch_end]
        batch_ids = chunk_ids[i:batch_end]

        print(f"Processing {i+1}-{batch_end} of {total}...")

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

    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    print(f"Done! {total} chunks indexed in {mins}m {secs}s.")
    return db


if __name__ == "__main__":
    index_documents(reset=True)
