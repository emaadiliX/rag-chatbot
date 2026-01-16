CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

    :root {
        --primary: #8b5cf6;
        --primary-light: #ddd6fe;
        --background-light: #f8fafc;
        --surface-light: #ffffff;
        --slate-50: #f8fafc;
        --slate-100: #f1f5f9;
        --slate-200: #e2e8f0;
        --slate-300: #cbd5e1;
        --slate-400: #94a3b8;
        --slate-500: #64748b;
        --slate-600: #475569;
        --slate-700: #334155;
        --slate-800: #1e293b;
        --slate-900: #0f172a;
        --indigo-50: #eef2ff;
        --indigo-100: #e0e7ff;
        --indigo-300: #a5b4fc;
        --indigo-500: #6366f1;
        --indigo-600: #4f46e5;
        --red-50: #fef2f2;
        --red-100: #fee2e2;
        --red-500: #ef4444;
        --green-500: #22c55e;
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
    }

    .stApp {
        background: var(--background-light);
    }

    .main .block-container {
        max-width: 1200px;
        padding: 1rem 2rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .main-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem 0 1.5rem 0;
        text-align: center;
    }

    .header-icon {
        width: 56px;
        height: 56px;
        background: var(--surface-light);
        border-radius: 16px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--slate-100);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.25rem;
        font-size: 1.75rem;
        position: relative;
    }

    .header-icon::after {
        content: '';
        position: absolute;
        bottom: -4px;
        right: -4px;
        width: 20px;
        height: 20px;
        background: var(--green-500);
        border-radius: 50%;
        border: 3px solid white;
    }

    .main-header h1 {
        color: var(--slate-900);
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: var(--slate-500);
        font-size: 0.95rem;
        max-width: 500px;
        line-height: 1.6;
        margin: 0;
    }

    section[data-testid="stSidebar"] {
        background: var(--surface-light);
        border-right: 1px solid var(--slate-200);
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .sidebar-section { margin-bottom: 1.5rem; }

    .sidebar-section-header {
        display: flex;
        align-items: center;
        gap: 0.625rem;
        margin-bottom: 0.75rem;
        color: var(--slate-500);
    }

    .sidebar-section-header .material-icons-round { font-size: 18px; }

    .sidebar-section-header h3 {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0;
    }

    .sidebar-about-text {
        font-size: 0.8125rem;
        line-height: 1.7;
        color: var(--slate-500);
        padding-left: 1.75rem;
    }

    .capability-item {
        display: flex;
        align-items: flex-start;
        font-size: 0.8125rem;
        padding-left: 1.75rem;
        margin-bottom: 0.75rem;
    }

    .capability-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(139, 92, 246, 0.6);
        margin-top: 6px;
        margin-right: 0.625rem;
    }

    .capability-text { color: var(--slate-600); }

    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    .user-message-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        margin-bottom: 1.5rem;
    }

    .user-message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .user-label {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--slate-400);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .user-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: var(--slate-200);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .user-avatar .material-icons-round {
        font-size: 14px;
        color: var(--slate-400);
    }

    .user-message {
        background: var(--surface-light);
        color: var(--slate-800);
        padding: 1.25rem;
        border-radius: 16px;
        border-top-right-radius: 4px;
        max-width: 85%;
        font-size: 0.9375rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        border: 1px solid var(--slate-100);
    }

    .assistant-message-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        width: 100%;
    }

    .assistant-message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .assistant-avatar {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        background: var(--indigo-600);
        color: white;
    }

    .assistant-avatar .material-icons-round { font-size: 14px; }

    .assistant-label {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--indigo-600);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .assistant-message {
        background: rgba(238, 242, 255, 0.4);
        border: 1px solid rgba(224, 231, 255, 0.6);
        border-radius: 16px;
        border-top-left-radius: 4px;
        width: 100%;
    }

    .assistant-message-content {
        padding: 1.5rem;
        font-size: 0.9375rem;
        line-height: 1.7;
        color: var(--slate-700);
    }

    .no-answer {
        background: var(--red-50);
        border-left: 3px solid var(--red-500);
        padding: 1rem 1.25rem;
        border-radius: 0 12px 12px 0;
        color: #991b1b;
        font-size: 0.9375rem;
    }

    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0;
    }

    .thinking-dot {
        width: 10px;
        height: 10px;
        background: var(--indigo-500);
        border-radius: 50%;
        animation: pulse 1.5s ease-in-out infinite;
    }

    .thinking-text {
        color: var(--slate-500);
        font-size: 0.875rem;
        font-style: italic;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    .source-card {
        display: flex;
        gap: 1rem;
        align-items: center;
        background: white;
        border: 1px solid var(--slate-200);
        border-radius: 12px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }

    .source-card:hover {
        border-color: var(--indigo-300);
    }

    .source-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background: var(--red-50);
        color: var(--red-500);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .source-icon .material-icons-round { font-size: 20px; }

    .source-info { flex: 1; }

    .source-info-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.75rem;
    }

    .source-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--slate-900);
    }

    .source-page {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--indigo-600);
        background: var(--indigo-50);
        padding: 0.25rem 0.625rem;
        border-radius: 6px;
    }

    .source-card a { color: inherit; text-decoration: none; }

    .examples-section { padding: 1rem 0; }

    .examples-title {
        font-size: 0.625rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--slate-400);
        margin-bottom: 0.75rem;
        text-align: center;
    }

    .input-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.75rem;
        color: var(--slate-400);
    }

    .input-footer .material-icons-round { font-size: 12px; }
    .input-footer span { font-size: 0.625rem; }

    .stChatMessage { background: transparent !important; }
    .streamlit-expanderHeader { font-size: 0.8rem !important; }
    .stSlider > div > div > div { background: var(--slate-200) !important; }
    .stSlider > div > div > div > div { background: var(--primary) !important; }
    .stButton > button { border-radius: 12px !important; }

    .stChatInput > div {
        border-radius: 20px !important;
        border: 1px solid var(--slate-200) !important;
        background: white !important;
    }

    .stDeployButton, [data-testid="stDecoration"], [data-testid="stToolbar"] {
        display: none !important;
    }
</style>
"""
