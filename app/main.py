import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from app.styles import CUSTOM_CSS
from app.source_links import PDF_URLS
from rag.retrieval import get_vector_db
from rag.prompting import ask, IDK_FALLBACK


@st.cache_resource(show_spinner=False)
def warm_up_vector_db():
    try:
        get_vector_db()
        return True
    except FileNotFoundError:
        return False


st.set_page_config(
    page_title="FinWise RAG Chat",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

db_ready = warm_up_vector_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "settings" not in st.session_state:
    st.session_state.settings = {"k": 5}

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:
    st.markdown('<p class="sidebar-label">ABOUT</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="sidebar-text">
        This assistant answers questions using a curated knowledge base of banking and financial regulatory documents.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">CAPABILITIES</p>',
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
    <div style="margin-bottom: 1.5rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">SETTINGS</p>',
                unsafe_allow_html=True)

    k = st.session_state.settings["k"]
    st.markdown(f"""
    <div class="slider-label-row">
        <span class="slider-label-text">Number of sources</span>
        <span class="slider-value">{k}</span>
    </div>
    """, unsafe_allow_html=True)

    st.slider(
        "Number of sources",
        min_value=1,
        max_value=10,
        value=k,
        key="k_slider",
        label_visibility="collapsed",
    )
    st.session_state.settings["k"] = st.session_state.k_slider

    st.markdown("""
    <div class="settings-range">
        <span>MIN: 1</span>
        <span>MAX: 10</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    if st.button("🗑  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()


st.markdown("""
<div class="main-header">
    <div class="header-icon">🏛️</div>
    <h1>FinWise RAG Chat</h1>
    <p>Interrogate banking regulations and financial disclosures with enterprise-grade precision.</p>
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

    with st.expander(f"📎 View sources ({len(sources)})", expanded=False):
        for s in sources:
            filename, page_part = parse_source_string(s)
            url = PDF_URLS.get(filename)
            page_badge = page_part.capitalize() if page_part else ""
            icon = "picture_as_pdf" if url else "description"

            if url:
                title_html = f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="source-title">{filename}</a>'
            else:
                title_html = f'<span class="source-title">{filename}</span>'

            page_span = f'<span class="source-page">{page_badge}</span>' if page_badge else ''

            st.markdown(f"""
            <div class="source-card">
                <div class="source-icon">
                    <span class="material-icons-round">{icon}</span>
                </div>
                <div class="source-info">
                    <div class="source-info-header">
                        {title_html}
                        {page_span}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


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
            <div class="user-avatar">
                <span class="material-icons-round">person</span>
            </div>
        </div>
        <div class="user-message">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def render_assistant_message(content, sources=None, animate=False, placeholder=None):
    if animate and placeholder:
        type_out_markdown(placeholder, content)
    else:
        st.markdown(f"""
        <div class="assistant-message-wrapper">
            <div class="assistant-message-header">
                <div class="assistant-avatar">
                    <span class="material-icons-round">auto_awesome</span>
                </div>
                <span class="assistant-label">FinWise AI</span>
            </div>
            <div class="assistant-message">
                <div class="assistant-message-content">{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if sources:
        render_sources(sources)


def handle_question(question):
    k = st.session_state.settings["k"]

    st.session_state.messages.append({"role": "user", "content": question})

    render_user_message(question)
    st.markdown("""
    <div class="assistant-message-wrapper">
        <div class="assistant-message-header">
            <div class="assistant-avatar">
                <span class="material-icons-round">auto_awesome</span>
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
            <span class="thinking-text">Searching knowledge base...</span>
        </div>
        """, unsafe_allow_html=True)

        result = ask(question, k=k, use_mmr=True)

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
                        <span class="material-icons-round">auto_awesome</span>
                    </div>
                    <span class="assistant-label">FinWise AI</span>
                </div>
                <div class="no-answer">🤷 {msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_assistant_message(msg["content"], msg.get("sources", []))
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="examples-section">
        <div class="examples-title">Try these examples</div>
    </div>
    """, unsafe_allow_html=True)

    examples = [
        "What are the Basel III capital requirements?",
        "What is the capital conservation buffer?",
        "What are the minimum CET1 requirements?",
    ]

    cols = st.columns(3)
    for col, example in zip(cols, examples):
        with col:
            if st.button(example, key=f"example_{example[:20]}", use_container_width=True):
                st.session_state.pending_question = example
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
user_input = st.chat_input("Ask FinWise about your documents...")
st.markdown("""
<div class="input-footer">
    <span class="material-icons-round">lock</span>
    <span>Encrypted & Confidential.</span>
</div>
""", unsafe_allow_html=True)

if user_input and user_input.strip():
    handle_question(user_input.strip())
