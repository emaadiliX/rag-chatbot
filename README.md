# Banking RAG Chatbot

A Retrieval-Augmented Generation chatbot for banking/financial documents.

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/emaadiliX/rag-chatbot.git
   cd rag-chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r Requirements.txt
   ```

4. **Configure environment**
   
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. **Add documents**
   
   Place your PDF documents in `data/documents/`

## How to Run

### 1. Index your documents (first time only)
```bash
python -m rag.indexing
```
This creates the vector database from your PDFs. It only needs to run once and takes approximately 10-15 minutes depending on the number of documents. The database is saved locally and reused on subsequent runs.

### 2. Launch the chatbot
```bash
streamlit run app/main.py
```

## Tech Stack

- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
