import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # noqa: E402

import time  # noqa: E402
import streamlit as st  # noqa: E402
from rag.retrieval import get_vector_db, get_reranker  # noqa: E402
from rag.prompting import ask, IDK_FALLBACK  # noqa: E402
from app.styles import CUSTOM_CSS  # noqa: E402
from app.source_links import PDF_URLS  # noqa: E402


@st.cache_resource(show_spinner=False)
def warm_up_models():
    try:
        get_vector_db()
        get_reranker()
        return True
    except FileNotFoundError:
        return False


st.set_page_config(
    page_title="FinWise Chat",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

db_ready = warm_up_models()

if "messages" not in st.session_state:
    st.session_state.messages = []


if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:
    st.markdown('<p class="sidebar-label">About</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="sidebar-text">
        This assistant answers questions using a curated knowledge base of banking and financial regulatory documents.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>",
                unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">Capabilities</p>',
                unsafe_allow_html=True)
    st.markdown("""
    <div class="capability-item">
        <span class="capability-dot"></span>
        <span class="capability-text">Grounded answers with citations</span>
    </div>
    <div class="capability-item">
        <span class="capability-dot"></span>
        <span class="capability-text">Source document references</span>
    </div>
    <div class="capability-item">
        <span class="capability-dot"></span>
        <span class="capability-text">Safe "I don't know" responses</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>",
                unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='margin-bottom: 1.5rem;'></div>",
                unsafe_allow_html=True)

    st.markdown("""
    <p class="sidebar-label" style="display: flex; align-items: center; gap: 0.5rem;">
        Number of sources
        <span class="material-symbols-outlined" title="Maximum number of documents to retrieve for answering your question" style="font-size: 14px; color: var(--text-muted); cursor: help;">help</span>
    </p>
    """, unsafe_allow_html=True)

    if "k_slider" not in st.session_state:
        st.session_state.k_slider = 5

    st.slider(
        "Number of sources",
        min_value=1,
        max_value=10,
        key="k_slider",
        label_visibility="collapsed",
    )

    st.markdown("<div style='flex-grow: 1; min-height: 2rem;'></div>",
                unsafe_allow_html=True)

    if st.button("🗑  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


st.markdown("""
<div class="main-header">
    <div class="header-row">
        <div class="header-text">
            <h1>FinWise Chat</h1>
            <p class="subtitle">Professional Financial Intelligence Assistant</p>
        </div>
    </div>
    <p>Interrogate banking regulations, capital requirements, and financial disclosures with enterprise-grade precision.</p>
</div>
""", unsafe_allow_html=True)


def parse_source_string(s):
    s = s.strip()
    if "(" in s and s.endswith(")"):
        left, right = s.rsplit("(", 1)
        filename = left.strip()
        page_part = right[:-1].strip()
        return filename, page_part
    return s, ""


def render_sources(sources):
    if not sources:
        return

    st.markdown(f"""
    <div class="sources-section">
        <div class="sources-header">
            <div class="sources-title">
                <span class="material-symbols-outlined">menu_book</span>
                Sources & Citations
            </div>
            <span class="sources-count">{len(sources)} documents</span>
        </div>
    """, unsafe_allow_html=True)

    for s in sources:
        filename, page_part = parse_source_string(s)
        url = PDF_URLS.get(filename)
        page_badge = page_part.upper() if page_part else ""

        if url:
            title_html = f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="source-title">{filename}</a>'
        else:
            title_html = f'<span class="source-title">{filename}</span>'

        page_span = f'<span class="source-page">{page_badge}</span>' if page_badge else ''

        st.markdown(f"""
        <div class="source-card">
            <div class="source-card-header">
                <div class="source-card-title">
                    <span class="material-symbols-outlined">description</span>
                    {title_html}
                </div>
                {page_span}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def type_out_markdown(target_placeholder, full_text, speed=0.0015):
    buf = ""
    for ch in full_text:
        buf += ch
        target_placeholder.markdown(buf)
        time.sleep(speed)


def render_user_message(content):
    st.markdown(f"""
    <div class="user-message-wrapper">
        <div class="user-message-header">
            <span class="user-label">You</span>
        </div>
        <div class="user-message">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_assistant_message(content, sources=None):
    st.markdown(f"""
    <div class="assistant-message-wrapper">
        <div class="assistant-message-header">
            <div class="assistant-avatar">
                <span class="material-symbols-outlined">auto_awesome</span>
            </div>
            <span class="assistant-label">Assistant</span>
        </div>
        <div class="assistant-message">
            <div class="assistant-message-content">{content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if sources:
        render_sources(sources)


def handle_question(question):
    k = st.session_state.k_slider

    chat_history = list(st.session_state.messages)

    st.session_state.messages.append({"role": "user", "content": question})

    render_user_message(question)
    st.markdown("""
    <div class="assistant-message-wrapper">
        <div class="assistant-message-header">
            <div class="assistant-avatar">
                <span class="material-symbols-outlined">auto_awesome</span>
            </div>
            <span class="assistant-label">Assistant</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    answer_box = st.empty()

    try:
        answer_box.markdown("""
        <div class="thinking-indicator">
            <span class="thinking-dot"></span>
            <span class="thinking-text">Searching documents...</span>
        </div>
        """, unsafe_allow_html=True)

        result = ask(question, k=k, chat_history=chat_history)

        answer_text = result.get("answer", IDK_FALLBACK)
        sources = result.get("sources", [])

        if IDK_FALLBACK in answer_text:
            answer_box.markdown(
                f'<div class="no-answer">🤷 {answer_text}</div>', unsafe_allow_html=True)
        else:
            type_out_markdown(answer_box, answer_text, speed=0.002)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer_text, "sources": sources}
        )

        render_sources(sources)

    except FileNotFoundError:
        msg = "I couldn't access the document database. Please run indexing first."
        answer_box.markdown(
            f'<div class="no-answer">🤷 {msg}</div>', unsafe_allow_html=True)
        st.session_state.messages.append(
            {"role": "assistant", "content": msg, "sources": []})
    except Exception:
        msg = "Sorry, I encountered an error while processing your question."
        answer_box.markdown(
            f'<div class="no-answer">🤷 {msg}</div>', unsafe_allow_html=True)
        st.session_state.messages.append(
            {"role": "assistant", "content": msg, "sources": []})

    st.rerun()


if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    handle_question(q)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_user_message(msg["content"])
    else:
        if IDK_FALLBACK in msg["content"]:
            st.markdown(f"""
            <div class="assistant-message-wrapper">
                <div class="assistant-message-header">
                    <div class="assistant-avatar">
                        <span class="material-symbols-outlined">auto_awesome</span>
                    </div>
                    <span class="assistant-label">Assistant</span>
                </div>
                <div class="no-answer"> {msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_assistant_message(msg["content"], msg.get("sources", []))
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="examples-section">
        <div class="examples-title">Suggested Topics</div>
    </div>
    """, unsafe_allow_html=True)

    examples = [
        "Basel III capital requirements",
        "Capital conservation buffer",
        "Minimum CET1 requirements",
    ]

    cols = st.columns(3)
    for col, example in zip(cols, examples):
        with col:
            if st.button(example, key=f"example_{example[:20]}", use_container_width=True):
                st.session_state.pending_question = example
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Use container so chat_input is inline (not auto-pinned), then pin via CSS
with st.container():
    user_input = st.chat_input("Analyze a document or ask a question...")

st.markdown("""
<div class="input-footer">
    <span class="material-symbols-outlined">verified_user</span>
    <span>FinWise AI insights are based on official bank documentation.</span>
</div>
""", unsafe_allow_html=True)

if user_input and user_input.strip():
    handle_question(user_input.strip())
