import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "rag_docs"


class VectorStoreManager:
    """Singleton to ensure vector DB is only loaded once."""
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_db(self):
        if self._db is None:
            if not os.path.exists(CHROMA_PATH):
                raise FileNotFoundError(
                    f"Vector database not found at {CHROMA_PATH}. "
                    "Run indexing.py first."
                )

            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self._db = Chroma(
                collection_name=COLLECTION_NAME,
                persist_directory=CHROMA_PATH,
                embedding_function=embeddings
            )

        return self._db


def get_vector_db():
    manager = VectorStoreManager()
    return manager.get_db()


def retrieve_context(query, k=5, use_mmr=False):
    """
    Retrieve top-K relevant chunks for a query.

    Args:
        query: User question
        k: Number of chunks to retrieve
        use_mmr: Use MMR for diversity

    Returns:
        List of (document, score) tuples
    """
    db = get_vector_db()

    if use_mmr:
        docs = db.max_marginal_relevance_search(query, k=k, fetch_k=k*3)
        return [(doc, None) for doc in docs]

    return db.similarity_search_with_score(query, k=k)


def format_retrieved_context(results):
    """
    Format chunks into context string with proper source numbering.

    Args:
        results: List of (document, score) tuples

    Returns:
        tuple: (context_string, citations_list)
    """
    if not results:
        return "", []

    context_parts = []
    citations = []
    seen_content = set()
    source_num = 1

    for doc, score in results:
        content = doc.page_content.strip()

        # Skip duplicates
        if content in seen_content:
            continue
        seen_content.add(content)

        source_doc = doc.metadata.get("source", "Unknown")
        page_num = doc.metadata.get("page", "?")

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

    results = retrieve_context(query, k=5)
    context, citations = format_retrieved_context(results)

    print(f"Found {len(citations)} relevant chunks:\n")
    for i, cit in enumerate(citations, 1):
        print(f"{i}. {cit['source']} (page {cit['page']})")

    print(f"\nContext preview:\n{context[:300]}...")
