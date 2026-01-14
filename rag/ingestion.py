import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdfs(data_dir: str = "data/documents") -> list:
    """
    Load all PDFs from the data directory.
    Returns a list of Document objects with page content and metadata.
    """
    documents = []
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(f"Directory not found: {data_dir}")

    pdf_files = list(data_path.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(f"No PDF files found in {data_dir}")

    print(f"Found {len(pdf_files)} PDF files")

    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path.name}")
        try:
            loader = PyPDFLoader(str(pdf_path))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = pdf_path.name

            documents.extend(docs)
        except Exception as e:
            print(f"Error loading {pdf_path.name}: {e}")
            continue

    print(f"Loaded {len(documents)} pages total")
    return documents


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and PDF artifacts.
    """
    text = " ".join(text.split())

    artifacts = [
        "Page |",
        "| Page",
        "\x00",  # Null characters
    ]
    for artifact in artifacts:
        text = text.replace(artifact, "")

    return text.strip()


def chunk_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """
    Split documents into smaller chunks for embedding.

    Args:
        documents: List of Document objects from load_pdfs()
        chunk_size: Target size of each chunk in characters
        chunk_overlap: Overlap between chunks to preserve context

    Returns:
        List of chunked Document objects
    """
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    documents = [doc for doc in documents if doc.page_content.strip()]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    print(f"Created {len(chunks)} chunks from {len(documents)} pages")
    return chunks


def run_ingestion(data_dir: str = "data/documents") -> list:
    """
    Run the full ingestion pipeline.

    Args:
        data_dir: Path to folder containing PDFs

    Returns:
        List of chunks ready for embedding
    """
    print("Starting ingestion...")
    print("=" * 50)

    documents = load_pdfs(data_dir)

    chunks = chunk_documents(documents)

    print("=" * 50)
    print(f"Ingestion complete: {len(chunks)} chunks ready")

    return chunks


if __name__ == "__main__":
    chunks = run_ingestion()

    # Preview first chunk
    if chunks:
        print("\n--- Sample Chunk ---")
        print(f"Source: {chunks[0].metadata['source']}")
        print(f"Page: {chunks[0].metadata.get('page', 'N/A')}")
        print(f"Content preview: {chunks[0].page_content[:300]}...")
