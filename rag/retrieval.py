import os
import re
import zipfile
import urllib.request
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from sentence_transformers import CrossEncoder

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"
RELEVANCE_THRESHOLD = 1.5

GDRIVE_FILE_ID = "1i10PzY9uhHwYtTBaXCsT_EQ61U3FbNrs"


def download_chroma_db():
    """Download and extract ChromaDB from Google Drive if not present locally."""
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        return

    print("Downloading vector database from Google Drive...")
    zip_path = "chroma_db.zip"

    try:
        import gdown
        url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
        gdown.download(url, zip_path, quiet=False)

        print("Extracting database...")
        os.makedirs(CHROMA_PATH, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(CHROMA_PATH)

        os.remove(zip_path)
        print("Vector database ready.")
    except Exception as e:
        print(f"Failed to download database: {e}")
        raise FileNotFoundError(
            f"Could not download vector database. Error: {e}"
        )

UNSAFE_PATTERNS = [
    r"ignore (all|any|previous|above) instructions",
    r"system prompt",
    r"override",
    r"forget your",
    r"new instructions",
    r"jailbreak",
    r"developer mode",
    r"\bDAN\b",
]


def is_safe_content(text):
    """Check if document content is safe (no injection patterns)."""
    if not text:
        return True
    return not any(re.search(p, text, flags=re.IGNORECASE) for p in UNSAFE_PATTERNS)


_cached_db = None
_cached_reranker = None


def get_vector_db():
    global _cached_db

    if _cached_db is None:
        if not os.path.exists(CHROMA_PATH) or not os.listdir(CHROMA_PATH):
            download_chroma_db()

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        _cached_db = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )

    return _cached_db


def get_reranker():
    global _cached_reranker

    if _cached_reranker is None:
        _cached_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    return _cached_reranker


def rerank_results(query, docs_with_scores, top_k=5):
    """Re-score documents using a cross-encoder for better relevance ranking."""
    if not docs_with_scores:
        return []

    reranker = get_reranker()

    pairs = [(query, doc.page_content) for doc, _ in docs_with_scores]

    rerank_scores = reranker.predict(pairs)

    reranked = list(zip(docs_with_scores, rerank_scores))
    reranked.sort(key=lambda x: x[1], reverse=True)

    results = [(doc, float(rerank_score))
               for (doc, _), rerank_score in reranked[:top_k]]

    return results


def retrieve_context(query, k=5):
    db = get_vector_db()

    initial_results = db.similarity_search_with_score(query, k=k * 2)

    filtered = [
        (doc, score) for doc, score in initial_results
        if score <= RELEVANCE_THRESHOLD and is_safe_content(doc.page_content)
    ]

    if not filtered:
        return []

    reranked = rerank_results(query, filtered, top_k=k)

    return reranked


def format_retrieved_context(results):
    if not results:
        return "", []

    context_parts = []
    citations = []
    seen_content = set()
    source_num = 1

    for doc, score in results:
        content = doc.page_content.strip()

        if content in seen_content:
            continue
        seen_content.add(content)

        source_doc = doc.metadata.get("source", "Unknown")
        page_num = doc.metadata.get("page", 0) + 1

        context_parts.append(
            f"[Source {source_num}: {source_doc}, Page {page_num}]\n{content}"
        )

        citations.append({
            "source": source_doc,
            "page": page_num,
            "score": None if score is None else float(score)
        })

        source_num += 1

    context = "\n\n---\n\n".join(context_parts)
    return context, citations


if __name__ == "__main__":
    query = "What are the Basel III capital requirements?"

    print(f"Query: {query}\n")
    print("Loading reranker model (first run may take a moment)...\n")

    results = retrieve_context(query, k=5)
    context, citations = format_retrieved_context(results)

    print(f"Found {len(citations)} relevant chunks (reranked):\n")
    for i, cit in enumerate(citations, 1):
        score = cit['score']
        # Higher rerank score = more relevant
        score_str = f" (rerank score: {score:.3f})" if score is not None else ""
        print(f"{i}. {cit['source']} (page {cit['page']}){score_str}")

    print(f"\nContext preview:\n{context[:500]}...")
