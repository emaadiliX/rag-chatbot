CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {
        --primary: #b5a2d9;
        --secondary: #f8e1eb;
        --accent-red: #e67e7e;
        --sidebar-bg: #ffffff;
        --main-bg: #fdfbfc;
        --text-dark: #2d2733;
        --text-muted: #8a8196;
        --lavender-bubble: #f6f3fc;
        --border-light: #f0edf5;
    }

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        box-sizing: border-box;
    }

    .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 20;
        display: inline-block;
        vertical-align: middle;
    }

    .stApp {
        background: var(--main-bg);
    }

    .main .block-container {
        max-width: 1200px;
        padding: 1rem 2rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border-light);
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 2rem;
    }

    .sidebar-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: var(--text-dark);
        text-transform: uppercase;
        margin-bottom: 1rem;
        opacity: 0.8;
    }

    .sidebar-text {
        font-size: 0.8125rem;
        line-height: 1.7;
        color: var(--text-muted);
    }

    .capability-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.8125rem;
        margin-bottom: 0.75rem;
    }

    .capability-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(181, 162, 217, 0.6);
        flex-shrink: 0;
    }

    .capability-text {
        color: var(--text-muted);
    }

    .slider-label-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .slider-label-text {
        display: flex;
        align-items: center;
        gap: 0.375rem;
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-dark);
    }

    .slider-value {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--accent-red);
        background: rgba(230, 126, 126, 0.1);
        padding: 0.125rem 0.5rem;
        border-radius: 0.375rem;
    }

    .settings-range {
        display: flex;
        justify-content: space-between;
        font-size: 0.625rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: -0.02em;
        margin-top: 0.5rem;
    }

    /* Main Header */
    .main-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 4rem 2rem 3rem 2rem;
        text-align: center;
    }

    .header-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .header-icon {
        width: 48px;
        height: 48px;
        background: white;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(181, 162, 217, 0.08);
        border: 1px solid var(--border-light);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }

    .header-text h1 {
        color: var(--text-dark);
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        text-align: left;
    }

    .header-text .subtitle {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        margin: 0;
        text-align: left;
    }

    .main-header > p {
        color: var(--text-muted);
        font-size: 0.8125rem;
        max-width: 28rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Chat Container */
    .chat-container {
        max-width: 48rem;
        margin: 0 auto;
        padding-bottom: 1rem;
    }

    /* User Message */
    .user-message-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        margin-bottom: 2.5rem;
    }

    .user-message-header {
        padding: 0 0.5rem;
        margin-bottom: 0.5rem;
    }

    .user-label {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .user-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: var(--border-light);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .user-avatar .material-symbols-outlined {
        font-size: 14px;
        color: var(--text-muted);
    }

    .user-message {
        max-width: 85%;
        background: var(--lavender-bubble);
        color: var(--text-dark);
        padding: 1rem 1.25rem;
        border-radius: 1rem;
        border-top-right-radius: 0;
        font-size: 0.8125rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(181, 162, 217, 0.08);
        border: 1px solid rgba(181, 162, 217, 0.1);
    }

    /* Assistant Message */
    .assistant-message-wrapper {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 2.5rem;
        width: 100%;
    }

    .assistant-message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0 0.5rem;
        margin-bottom: 0.5rem;
    }

    .assistant-avatar {
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: rgba(181, 162, 217, 0.1);
    }

    .assistant-avatar .material-symbols-outlined {
        font-size: 12px;
        color: var(--primary);
    }

    .assistant-label {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .assistant-message {
        max-width: 90%;
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 1rem;
        border-top-left-radius: 0;
        box-shadow: 0 4px 20px rgba(181, 162, 217, 0.08);
    }

    .assistant-message-content {
        padding: 1.5rem;
        font-size: 0.8125rem;
        line-height: 1.6;
        color: var(--text-dark);
    }

    .assistant-message-content strong {
        color: var(--text-dark);
        font-weight: 600;
    }

    .assistant-message-content ul {
        margin: 1rem 0 0 0;
        padding: 0;
        list-style: none;
    }

    .assistant-message-content li {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        color: var(--text-muted);
        font-size: 0.8125rem;
    }

    .assistant-message-content li::before {
        content: '•';
        color: var(--primary);
        flex-shrink: 0;
    }

    /* Thinking Indicator */
    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: var(--lavender-bubble);
        border: 1px solid var(--border-light);
        border-radius: 0.75rem;
    }

    .thinking-dot {
        width: 8px;
        height: 8px;
        background: var(--primary);
        border-radius: 50%;
        animation: pulse 1.5s ease-in-out infinite;
    }

    .thinking-text {
        color: var(--text-muted);
        font-size: 0.8125rem;
        font-style: italic;
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    /* No Answer / Error */
    .no-answer {
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 1rem 1.25rem;
        border-radius: 0 0.75rem 0.75rem 0;
        color: #991b1b;
        font-size: 0.8125rem;
    }

    /* Sources Section */
    .sources-section {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border-light);
    }

    .sources-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .sources-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-dark);
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .sources-title .material-symbols-outlined {
        font-size: 18px;
        color: var(--primary);
    }

    .sources-count {
        font-size: 0.625rem;
        font-weight: 500;
        color: var(--text-muted);
        background: var(--border-light);
        padding: 0.125rem 0.5rem;
        border-radius: 0.25rem;
    }

    .source-card {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .source-card:hover {
        border-color: rgba(181, 162, 217, 0.3);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    .source-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 0.5rem;
    }

    .source-card-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        overflow: hidden;
    }

    .source-card-title .material-symbols-outlined {
        font-size: 18px;
        color: var(--text-muted);
    }

    .source-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-dark);
        text-decoration: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .source-title:hover {
        color: var(--primary);
    }

    .source-page {
        font-size: 0.625rem;
        font-weight: 700;
        color: var(--primary);
        background: rgba(181, 162, 217, 0.05);
        padding: 0.125rem 0.5rem;
        border-radius: 9999px;
        border: 1px solid rgba(181, 162, 217, 0.1);
        flex-shrink: 0;
    }

    .source-excerpt {
        font-size: 0.6875rem;
        color: var(--text-muted);
        font-style: italic;
        line-height: 1.6;
        padding-left: 1.5rem;
        border-left: 2px solid rgba(181, 162, 217, 0.2);
    }

    .source-card a {
        color: inherit;
        text-decoration: none;
    }

    /* Examples Section */
    .examples-section {
        padding: 2rem 0;
    }

    .examples-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .examples-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.75rem;
    }

    /* Footer */
    .input-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .input-footer .material-symbols-outlined {
        font-size: 12px;
        color: var(--text-muted);
    }

    .input-footer span {
        font-size: 0.625rem;
        font-weight: 500;
        color: var(--text-muted);
        letter-spacing: 0.02em;
    }

    /* Streamlit Overrides */
    .stChatMessage {
        background: transparent !important;
    }

    /* Sources expander styling */
    .stExpander {
        border: none !important;
        border-top: 1px solid var(--border-light) !important;
        border-radius: 0 !important;
        background: transparent !important;
        margin-top: 1.5rem !important;
        padding-top: 1rem !important;
    }

    .stExpander summary {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        color: var(--text-dark) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.02em !important;
    }

    .stExpander summary:hover {
        color: var(--primary) !important;
    }

    .stExpander summary svg {
        color: var(--primary) !important;
    }

    .streamlit-expanderContent {
        border: none !important;
        padding: 1rem 0 0 0 !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: #f1f1f1 !important;
        height: 4px !important;
    }

    .stSlider > div > div > div > div {
        background: var(--accent-red) !important;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: var(--accent-red) !important;
        width: 16px !important;
        height: 16px !important;
        border: 2px solid white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 0.75rem !important;
        border: 1px solid var(--border-light) !important;
        background-color: white !important;
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        height: 3rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }

    .stButton > button:hover {
        background-color: var(--lavender-bubble) !important;
        color: var(--primary) !important;
    }

    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Example buttons */
    div[data-testid="column"] .stButton > button {
        background: white !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        color: var(--text-dark) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        height: auto !important;
    }

    div[data-testid="column"] .stButton > button:hover {
        border-color: rgba(181, 162, 217, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* Chat Input */
    .stChatInput > div {
        border-radius: 1rem !important;
        border: 1px solid var(--border-light) !important;
        background: white !important;
        box-shadow: 0 4px 20px rgba(181, 162, 217, 0.08) !important;
        padding: 0.375rem 0.375rem 0.375rem 1.25rem !important;
    }

    .stChatInput > div:focus-within {
        border-color: rgba(181, 162, 217, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(181, 162, 217, 0.1), 0 4px 20px rgba(181, 162, 217, 0.08) !important;
    }

    .stChatInput input {
        font-size: 0.8125rem !important;
    }

    .stChatInput input::placeholder {
        color: rgba(138, 129, 150, 0.6) !important;
    }

    .stChatInput button {
        background: var(--primary) !important;
        border-radius: 0.75rem !important;
        width: 2.5rem !important;
        height: 2.5rem !important;
    }

    .stChatInput button:hover {
        background: rgba(181, 162, 217, 0.9) !important;
    }

    /* Divider */
    .stDivider {
        border-color: var(--border-light) !important;
    }

    hr {
        border-color: var(--border-light) !important;
    }

    /* Hide Streamlit elements */
    .stDeployButton, [data-testid="stDecoration"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Expander styling */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }

    .stExpander > details > summary {
        padding: 0 !important;
        background: transparent !important;
    }

    .stExpander > details > div {
        padding: 0 !important;
        border: none !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #eeeaf2;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #dcd4e8;
    }
</style>
"""
