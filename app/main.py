import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from rag.prompting import ask, IDK_FALLBACK

st.set_page_config(
    page_title="Banking RAG Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .stApp { background: #f8fafc; }
    .main .block-container { max-width: 900px; padding: 2rem 1.5rem; }

    .main-header {
        text-align: center;
        padding: 2rem 0 2.5rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .main-header p { color: #64748b; font-size: 1rem; font-weight: 400; }

    .source-card {
        background: #f1f5f9;
        border-left: 3px solid #3b82f6;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.875rem;
        color: #334155;
    }
    .source-card strong { color: #0f172a; }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #0f172a;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #475569;
        font-size: 0.875rem;
        line-height: 1.6;
    }
    section[data-testid="stSidebar"] hr {
        margin: 1.5rem 0;
        border-color: #e2e8f0;
    }

    .no-answer {
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        color: #991b1b;
        font-size: 0.95rem;
    }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 2rem 0; }
    h3 { color: #0f172a; font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; }

    [data-testid="stMetricValue"] { color: #0f172a; font-size: 1.5rem; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #64748b; font-size: 0.875rem; font-weight: 500; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

if "settings" not in st.session_state:
    st.session_state.settings = {"k": 5, "use_mmr": False}

st.markdown(
    """
<div class="main-header">
    <h1>Banking RAG Assistant</h1>
    <p>Ask questions about Basel III, capital requirements, and banking regulations</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("---")
    st.markdown("## About")
    st.markdown(
        """
This assistant answers questions using a curated knowledge base of banking and financial regulatory documents.

**Features:**
- Grounded answers with citations
- Source document references
- Safe "I don't know" responses
"""
    )
    st.markdown("---")
    st.session_state.settings["k"] = st.slider(
        "Number of sources to retrieve",
        min_value=3,
        max_value=10,
        value=st.session_state.settings["k"],
        help="More sources = more comprehensive but slower",
    )


    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()

def render_sources(sources: list[str]) -> None:
    if not sources:
        return
    with st.expander(f"📚 View {len(sources)} source(s)", expanded=False):
        for i, s in enumerate(sources, 1):
            st.markdown(
                f"""
<div class="source-card">
    <strong>Source {i}:</strong> {s}
</div>
""",
                unsafe_allow_html=True,
            )


def type_out_markdown(target_placeholder, full_text: str, speed: float = 0.002) -> None:

    buf = ""
    for ch in full_text:
        buf += ch
        target_placeholder.markdown(buf)
        time.sleep(speed)


def handle_question(question: str) -> None:
    k = st.session_state.settings["k"]
    use_mmr = st.session_state.settings["use_mmr"]

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        status = st.empty()
        answer_box = st.empty()

        status.markdown("⏳ Retrieving relevant passages…")

        try:
            result = ask(question, k=k, use_mmr=use_mmr)

            status.markdown("✅ Generating answer…")

            answer_text = result.get("answer", IDK_FALLBACK)
            sources = result.get("sources", [])

            if IDK_FALLBACK in answer_text:
                answer_box.markdown(f'<div class="no-answer">🤷 {answer_text}</div>', unsafe_allow_html=True)
            else:
                type_out_markdown(answer_box, answer_text, speed=0.0015)
                render_sources(sources)

            status.empty()

            st.session_state.messages.append(
                {"role": "assistant", "content": answer_text, "sources": sources}
            )
            st.session_state.total_queries += 1

        except FileNotFoundError:
            status.empty()
            msg = "I couldn't access the document database. Please run indexing first."
            answer_box.markdown(f'<div class="no-answer">🤷 {msg}</div>', unsafe_allow_html=True)
            st.session_state.messages.append(
                {"role": "assistant", "content": msg, "sources": []}
            )
        except Exception:
            status.empty()
            msg = "Sorry, I encountered an error while processing your question."
            answer_box.markdown(f'<div class="no-answer">🤷 {msg}</div>', unsafe_allow_html=True)
            st.session_state.messages.append(
                {"role": "assistant", "content": msg, "sources": []}
            )

    st.rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and IDK_FALLBACK in msg["content"]:
            st.markdown(f'<div class="no-answer">🤷 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_sources(msg.get("sources", []))

st.markdown("---")

user_input = st.chat_input("Ask a question...")

if user_input and user_input.strip():
    handle_question(user_input.strip())

st.markdown("##### 💡 Try these examples:")
example_cols = st.columns(3)
examples = [
    "What are the Basel III capital requirements?",
    "What is the capital conservation buffer?",
    "What are the minimum CET1 requirements?",
]

for col, example in zip(example_cols, examples):
    with col:
        if st.button(example, key=f"example_{example[:24]}", use_container_width=True):
            handle_question(example)
