"""
NyayaSahayak - LLM-based Intelligent Legal Assistance System for Indian Laws
Streamlit Frontend - Modern, Stylish, Feature-Rich
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import html
import re
import random
import json
import uuid
from pathlib import Path
from datetime import datetime

# Voice input - optional dependency
try:
    from streamlit_mic_recorder import speech_to_text
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# Disable TensorFlow to avoid compatibility issues with transformers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['DISABLE_TF'] = '1'

import importlib.util
_original_find_spec = importlib.util.find_spec

def patched_find_spec(name, package=None):
    if name == 'tensorflow' or (isinstance(name, str) and name.startswith('tensorflow')):
        return None
    return _original_find_spec(name, package)

importlib.util.find_spec = patched_find_spec

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import backend.config as config
from backend.auth import AuthManager, render_auth_page

# Multilingual support
try:
    from frontend.multilingual_ui import (
        MultilingualUI,
        render_multilingual_sidebar,
        get_current_language_settings
    )
    MULTILINGUAL_AVAILABLE = True
except ImportError:
    MULTILINGUAL_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="NyayaSahayak - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CLEAN WHITE UI - Clear & Readable ==============
st.markdown("""
<style>
/* ==================== FONTS ==================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --primary-light: #3b82f6;
    --secondary: #059669;
    --accent: #dc2626;
    --bg-white: #ffffff;
    --bg-light: #f8fafc;
    --bg-gray: #f1f5f9;
    --text-dark: #1e293b;
    --text-body: #334155;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --border-dark: #cbd5e1;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
    --radius: 8px;
    --radius-lg: 12px;
}

/* ==================== BASE ==================== */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-light) !important;
    color: var(--text-body) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.main .block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
}

#MainMenu, footer, header {visibility: hidden !important;}
.stDeployButton {display: none !important;}

/* ==================== SIDEBAR ==================== */
[data-testid="stSidebar"] {
    background: var(--bg-white) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-dark) !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin: 1rem 0 0.75rem 0 !important;
}

[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.625rem 1.25rem !important;
    border: none !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.2s ease !important;
    min-height: 40px !important;
}

.stButton > button:hover {
    background: var(--primary-dark) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary buttons in sidebar */
[data-testid="stSidebar"] .stButton > button {
    background: var(--bg-gray) !important;
    color: var(--text-dark) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.8rem !important;
    padding: 0.5rem 0.75rem !important;
    min-height: 36px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--primary) !important;
    color: white !important;
    border-color: var(--primary) !important;
}

/* ==================== INPUTS ==================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius) !important;
    color: var(--text-dark) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Chat Input */
[data-testid="stChatInput"] {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-lg) !important;
}

[data-testid="stChatInput"] input {
    color: var(--text-dark) !important;
    font-size: 0.95rem !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
}

/* ==================== CHAT MESSAGES ==================== */
[data-testid="stChatMessage"] {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 1.25rem !important;
    margin: 0.75rem 0 !important;
    box-shadow: var(--shadow) !important;
}

/* ==================== EXPANDER ==================== */
.streamlit-expanderHeader {
    background: var(--bg-gray) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-dark) !important;
    font-weight: 600 !important;
    padding: 0.75rem 1rem !important;
}

.streamlit-expanderHeader:hover {
    background: var(--bg-light) !important;
}

.streamlit-expanderContent {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
    padding: 1rem !important;
}

/* ==================== HERO SECTION ==================== */
.hero-section {
    background: linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow-md);
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.9);
    font-weight: 400;
}

/* ==================== CARDS ==================== */
.premium-card, .info-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    margin: 0.75rem 0;
    box-shadow: var(--shadow);
}

.premium-card:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow-md);
}

.info-card {
    border-left: 4px solid var(--primary);
}

/* Source cards */
.source-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    margin: 0.5rem 0;
}

.source-card:hover {
    border-color: var(--primary);
}

.source-title {
    font-weight: 600;
    color: var(--text-dark);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.source-content {
    color: var(--text-body);
    font-size: 0.85rem;
    line-height: 1.6;
}

/* ==================== STICKY HEADER ==================== */
.sticky-header-container {
    background: var(--bg-white);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
    margin-bottom: 1rem;
}

.sticky-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 0.5rem;
}

/* ==================== TABS ==================== */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-gray) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-white) !important;
    color: var(--text-dark) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-white) !important;
    color: var(--primary) !important;
    box-shadow: var(--shadow) !important;
}

/* ==================== SELECT BOX ==================== */
.stSelectbox > div > div {
    background: var(--bg-white) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius) !important;
    color: var(--text-dark) !important;
}

.stSelectbox > div > div:hover {
    border-color: var(--primary) !important;
}

/* ==================== ALERTS ==================== */
.stAlert {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-body) !important;
}

[data-testid="stNotification"] {
    background: #eff6ff !important;
    border-left: 4px solid var(--primary) !important;
}

/* ==================== TYPOGRAPHY ==================== */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-dark) !important;
    font-family: 'Poppins', sans-serif !important;
}

p, span, div {
    color: var(--text-body);
}

.stMarkdown {
    color: var(--text-body) !important;
}

/* ==================== RADIO & CHECKBOX ==================== */
.stRadio > div {
    background: var(--bg-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem !important;
}

.stRadio label {
    color: var(--text-dark) !important;
    font-weight: 500 !important;
}

/* ==================== METRICS ==================== */
[data-testid="stMetricValue"] {
    color: var(--text-dark) !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
}

/* ==================== DIVIDER ==================== */
hr {
    border-color: var(--border) !important;
}

/* ==================== SCENARIO CARDS ==================== */
.scenario-card {
    background: var(--bg-white);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    margin: 0.75rem 0;
    transition: all 0.2s ease;
}

.scenario-card:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow-md);
}

.scenario-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: var(--text-dark);
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.scenario-desc {
    color: var(--text-body);
    font-size: 0.875rem;
    line-height: 1.5;
}

/* Emergency Card */
.emergency-card {
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-left: 4px solid var(--accent);
    border-radius: var(--radius);
    padding: 1rem;
}

.emergency-title {
    color: var(--accent);
    font-weight: 600;
    font-size: 0.9rem;
}

.emergency-number {
    color: var(--text-dark);
    font-weight: 700;
    font-size: 1.1rem;
}

/* ==================== MODE CARDS ==================== */
.mode-card {
    background: var(--bg-white);
    border: 2px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
    cursor: pointer;
}

.mode-card:hover {
    border-color: var(--primary);
    box-shadow: var(--shadow-md);
}

.mode-card.active {
    border-color: var(--primary);
    background: #eff6ff;
}

.mode-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
}

.mode-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: var(--text-dark);
    font-size: 1rem;
    margin-bottom: 0.25rem;
}

.mode-desc {
    color: var(--text-muted);
    font-size: 0.8rem;
}

/* ==================== COMPARISON TABLE ==================== */
.comparison-header {
    background: var(--primary);
    color: white;
    padding: 1rem;
    font-weight: 600;
    text-align: center;
    border-radius: var(--radius) var(--radius) 0 0;
}

.comparison-row {
    display: flex;
    border-bottom: 1px solid var(--border);
}

.comparison-cell {
    flex: 1;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    color: var(--text-body);
}

.comparison-cell:first-child {
    background: var(--bg-gray);
    font-weight: 600;
    color: var(--text-dark);
}

/* ==================== CIVIL/CRIMINAL ==================== */
.civil-header {
    background: var(--secondary);
}

.criminal-header {
    background: var(--accent);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "vector_store_initialized" not in st.session_state:
    st.session_state.vector_store_initialized = False
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_mode" not in st.session_state:
    st.session_state.query_mode = "general"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "voice_lang" not in st.session_state:
    st.session_state.voice_lang = "en"  # en or hi
if "card_shuffle_seed" not in st.session_state:
    st.session_state.card_shuffle_seed = random.randint(0, 9999)
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"  # chat, help, about
if "scenario_page" not in st.session_state:
    st.session_state.scenario_page = 1
if "help_page" not in st.session_state:
    st.session_state.help_page = 1
if "about_page" not in st.session_state:
    st.session_state.about_page = 1
if "civil_criminal_page" not in st.session_state:
    st.session_state.civil_criminal_page = 1
if "civil_criminal_tab" not in st.session_state:
    st.session_state.civil_criminal_tab = "overview"

# Chat persistence path
CHAT_STORAGE_PATH = parent_dir / "chat_history.json"


def load_chat_sessions():
    """Load saved chat sessions from disk"""
    try:
        if CHAT_STORAGE_PATH.exists():
            with open(CHAT_STORAGE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def save_chat_sessions(sessions):
    """Save chat sessions to disk"""
    try:
        with open(CHAT_STORAGE_PATH, "w", encoding="utf-8") as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def create_new_chat():
    """Create a new chat session"""
    sid = str(uuid.uuid4())[:8]
    new_session = {
        "id": sid,
        "title": "New Chat",
        "created": datetime.now().isoformat(),
        "messages": []
    }
    sessions = load_chat_sessions()
    sessions.insert(0, new_session)
    save_chat_sessions(sessions)
    st.session_state.chat_sessions = sessions
    st.session_state.current_session_id = sid
    return sid


def get_current_session():
    """Get current session or create one"""
    sessions = load_chat_sessions()
    if not sessions:
        create_new_chat()
        sessions = load_chat_sessions()
    elif not st.session_state.current_session_id:
        st.session_state.current_session_id = sessions[0]["id"]
    st.session_state.chat_sessions = sessions
    return next((s for s in sessions if s["id"] == st.session_state.current_session_id), None)


def _serialize_sources(sources):
    """Convert Document objects to JSON-serializable dicts"""
    out = []
    for doc in (sources or [])[:4]:
        try:
            out.append({
                "source": getattr(doc, "metadata", {}).get("source", "Legal Document"),
                "content": getattr(doc, "page_content", "")[:300]
            })
        except Exception:
            pass
    return out


def _deserialize_sources(sources_data):
    """Convert saved dicts back to object-like for render_source_cards"""
    class DocLike:
        def __init__(self, source, content):
            self.metadata = {"source": source}
            self.page_content = content
    return [DocLike(d["source"], d["content"]) for d in (sources_data or [])]


def add_to_session(session_id, query, answer, sources):
    """Add a message to a session and update title if first message"""
    sessions = load_chat_sessions()
    for s in sessions:
        if s["id"] == session_id:
            s["messages"].append({"q": query, "a": answer, "sources": _serialize_sources(sources)})
            if s["title"] == "New Chat":
                s["title"] = (query[:40] + "…") if len(query) > 40 else query
            break
    save_chat_sessions(sessions)
    st.session_state.chat_sessions = sessions


def get_session_messages(session_id):
    """Get messages for a session (sources as DocLike objects)"""
    sessions = load_chat_sessions()
    for s in sessions:
        if s["id"] == session_id:
            return [
                (m["q"], m["a"], _deserialize_sources(m.get("sources", [])))
                for m in s["messages"]
            ]
    return []


def clear_current_chat():
    """Clear messages from current session"""
    sessions = load_chat_sessions()
    for s in sessions:
        if s["id"] == st.session_state.current_session_id:
            s["messages"] = []
            s["title"] = "New Chat"
            break
    save_chat_sessions(sessions)
    st.session_state.chat_sessions = sessions


# ============== QUICK LEGAL CATEGORIES (Unique Feature #1) ==============
LEGAL_CATEGORIES = [
    {"id": "ipc", "icon": "📜", "title": "IPC / BNS Crimes", "query": "What are the provisions and punishments under Bharatiya Nyaya Sanhita or IPC for criminal offenses?", "desc": "Theft, Cheating, Assault, etc."},
    {"id": "arrest", "icon": "🚔", "title": "Arrest & Custody Rights", "query": "What are my rights during police arrest and custody under CrPC?", "desc": "Your rights when arrested"},
    {"id": "bail", "icon": "🔓", "title": "Bail Provisions", "query": "Explain bail provisions, types of bail, and procedure under Indian law", "desc": "Regular & anticipatory bail"},
    {"id": "consumer", "icon": "🛒", "title": "Consumer Rights", "query": "What are my rights under Consumer Protection Act for defective products or services?", "desc": "Refunds, compensation"},
    {"id": "cyber", "icon": "💻", "title": "Cyber Crimes", "query": "What are the punishments for cyber crimes like fraud, hacking under IT Act?", "desc": "Online offenses"},
    {"id": "women", "icon": "🛡️", "title": "Women's Protection", "query": "What legal protection do women have against domestic violence and harassment?", "desc": "DV Act, Protection orders"},
    {"id": "property", "icon": "🏠", "title": "Property Disputes", "query": "What are the legal provisions for property disputes and ownership in India?", "desc": "Land, inheritance"},
    {"id": "employment", "icon": "💼", "title": "Employment Law", "query": "What are employee rights regarding termination, wages, and workplace harassment?", "desc": "Labour laws"},
]

# Legal Jargon Glossary (Unique Feature #4 - Jargon Explainer)
LEGAL_GLOSSARY = {
    "IPC": "Indian Penal Code - Main criminal code of India",
    "BNS": "Bharatiya Nyaya Sanhita - New criminal code replacing IPC (2023)",
    "CrPC": "Code of Criminal Procedure - Procedure for criminal cases",
    "cognizable": "Offense where police can arrest without warrant",
    "non-cognizable": "Offense where police need warrant to arrest",
    "bail": "Release of accused before trial on security/surety",
    "anticipatory bail": "Bail sought before arrest in anticipation",
    "FIR": "First Information Report - Initial complaint to police",
    "bailable": "Offense where bail is a right",
    "non-bailable": "Offense where bail is at court's discretion",
    "compoundable": "Offense that can be settled between parties",
    "cognizance": "Court taking notice of an offense to start proceedings",
    "magistrate": "Judicial officer with limited jurisdiction",
    "summons": "Legal order to appear in court",
    "warrant": "Court order for arrest or search",
}

# Scenario templates - Extended list for dynamic rotation
SCENARIO_TEMPLATES = [
    "What happens if someone cheats me of ₹50,000? What are the legal provisions and punishments?",
    "What if I am arrested without being told the reason? What are my rights?",
    "What happens if I receive a defective product? What legal recourse do I have?",
    "What if I am a victim of domestic violence? What protection can I get?",
    "What happens if someone files a false case against me?",
    "What if my employer terminates me without notice? What are my rights?",
    "What if someone threatens me online? What are the cyber crime laws?",
    "What happens if my landlord evicts me without notice?",
    "What if I witness a crime? What are my legal obligations?",
    "What happens if I get a traffic challan? Can I appeal?",
]


def initialize_system():
    """Initialize the RAG system"""
    try:
        try:
            from backend.pdf_processor import PDFProcessor
        except Exception as e:
            st.error(f"Failed to import PDFProcessor: {str(e)}")
            return False

        try:
            from backend.vector_store import VectorStoreManager
        except Exception as e:
            st.error(f"Failed to import VectorStoreManager: {str(e)}")
            return False

        try:
            import backend.rag_chain as rag_chain_module
            if not hasattr(rag_chain_module, 'RAGChain'):
                st.error("RAGChain class not found")
                return False
            RAGChain = rag_chain_module.RAGChain
        except ImportError as e:
            st.error(f"Failed to import RAGChain: {str(e)}")
            return False

        with st.spinner("⚡ Initializing NyayaSahayak..."):
            if os.path.exists(config.VECTOR_STORE_PATH) and os.listdir(config.VECTOR_STORE_PATH):
                vector_store_manager = VectorStoreManager(config.VECTOR_STORE_PATH)
                vector_store_manager.load_vector_store()
            else:
                st.info("📚 First-time setup: Processing legal documents...")
                pdf_processor = PDFProcessor(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
                pdf_files = [f for f in config.PDF_FILES if os.path.exists(f)]
                if not pdf_files:
                    st.error("No PDF files found in project directory.")
                    return False
                documents = pdf_processor.process_multiple_pdfs(pdf_files)
                if not documents:
                    st.error("Could not process PDF documents.")
                    return False
                vector_store_manager = VectorStoreManager(config.VECTOR_STORE_PATH)
                vector_store_manager.create_vector_store(documents)
                vector_store_manager.save_vector_store()

            if not config.GOOGLE_API_KEY:
                st.error("⚠️ Set GOOGLE_API_KEY in .env file")
                return False

            rag_chain = RAGChain(vector_store_manager)
            st.session_state.rag_chain = rag_chain
            st.session_state.vector_store_initialized = True
            return True

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False


def render_source_cards(sources):
    """Render source evidence cards (Unique Feature #3)"""
    if not sources:
        return
    st.markdown("##### 📎 Source Evidence")
    for i, doc in enumerate(sources[:4], 1):
        source_name = html.escape(doc.metadata.get("source", "Legal Document"))
        raw = doc.page_content[:200].replace("\n", " ") + "..." if len(doc.page_content) > 200 else doc.page_content
        content_preview = html.escape(raw)
        st.markdown(f"""
        <div class="source-card">
            <strong>Source {i}:</strong> {source_name}<br>
            <span style="color:#64748b;font-size:0.85rem;">{content_preview}</span>
        </div>
        """, unsafe_allow_html=True)


def render_jargon_explainer(answer_text):
    """Extract and explain legal terms found in answer (Unique Feature #4)"""
    answer_upper = answer_text.upper()
    found_terms = []
    for term, explanation in LEGAL_GLOSSARY.items():
        if term.upper() in answer_upper and term not in [t[0] for t in found_terms]:
            found_terms.append((term, explanation))
    if found_terms:
        with st.expander("📖 Legal Terms in This Answer"):
            for term, explanation in found_terms[:8]:
                st.markdown(f"**{term}:** {explanation}")


def parse_answer_cards(answer_text):
    """Parse answer into structured cards (SUMMARY, KEY POINTS, LEGAL PROVISION, NEXT STEPS)"""
    cards = []
    text = answer_text.strip()
    # Flexible patterns - match **Section:** or Section: or ## Section
    patterns = [
        (r"\*\*SUMMARY:?\*\*\s*(.+?)(?=\*\*[A-Z\s]|\n\*\*|$)", "summary", "📌 Summary"),
        (r"\*\*KEY POINTS?:?\*\*\s*([\s\S]+?)(?=\*\*[A-Z\s]|\n\*\*[A-Z]|$)", "points", "🔑 Key Points"),
        (r"\*\*LEGAL PROVISION[S]?:?\*\*\s*([\s\S]+?)(?=\*\*[A-Z\s]|\n\*\*[A-Z]|$)", "law", "📜 Legal Provision"),
        (r"\*\*NEXT STEPS?:?\*\*\s*([\s\S]+?)(?=\*\*|$)", "steps", "✅ Next Steps"),
    ]
    for regex, card_type, title in patterns:
        m = re.search(regex, text, re.IGNORECASE | re.DOTALL)
        if m:
            content = m.group(1).strip()
            if content and len(content) > 3:
                # Truncate very long content for cards
                if len(content) > 600:
                    content = content[:600] + "..."
                cards.append({"type": card_type, "title": title, "content": content})
    if not cards:
        # Fallback: split by double newline or bullets into chunks
        parts = re.split(r'\n\n+', text)
        if len(parts) > 1:
            cards.append({"type": "summary", "title": "📌 Summary", "content": parts[0][:500]})
            for p in parts[1:3]:
                if p.strip() and len(p) > 20:
                    cards.append({"type": "points", "title": "📋 Details", "content": p[:400]})
        else:
            cards.append({"type": "summary", "title": "📌 Answer", "content": text[:800]})
    return cards


def render_answer_cards(answer_text):
    """Render answer in attractive card-based layout"""
    cards = parse_answer_cards(answer_text)
    for card in cards:
        content = html.escape(card["content"]).replace("\n", "<br>")
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'•\s*', r'• ', content)
        st.markdown(f"""
        <div class="answer-card {card['type']}">
            <div class="answer-card-title">{card['title']}</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)


def get_shuffled_categories():
    """Return categories in dynamic shuffled order (changes each session)"""
    cats = LEGAL_CATEGORIES.copy()
    random.seed(st.session_state.card_shuffle_seed)
    random.shuffle(cats)
    return cats


def get_shuffled_scenarios():
    """Return scenarios in dynamic shuffled order"""
    scenarios = SCENARIO_TEMPLATES.copy()
    random.seed(st.session_state.card_shuffle_seed + 1)
    random.shuffle(scenarios)
    return scenarios


def paginate_items(items, page_num, items_per_page=4):
    """Paginate a list of items. Returns (paginated_items, total_pages)"""
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    start_idx = (page_num - 1) * items_per_page
    end_idx = start_idx + items_per_page
    return items[start_idx:end_idx], total_pages


def render_pagination(current_page, total_pages, session_state_key):
    """Render pagination controls"""
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[0]:
        if current_page > 1:
            if st.button("⬅️ Previous", use_container_width=True, key=f"{session_state_key}_prev"):
                st.session_state[session_state_key] = current_page - 1
                st.rerun()
        else:
            st.write("")
    
    with cols[2]:
        st.markdown(f"<div style='text-align: center; padding: 0.5rem; color: #64748b; font-weight: 500;'>Page {current_page} of {total_pages}</div>", unsafe_allow_html=True)
    
    with cols[4]:
        if current_page < total_pages:
            if st.button("Next ➡️", use_container_width=True, key=f"{session_state_key}_next"):
                st.session_state[session_state_key] = current_page + 1
                st.rerun()
        else:
            st.write("")


def process_query(query_text: str) -> bool:
    """Process a query and add to current session. Returns True if processed."""
    if not query_text or not query_text.strip():
        return False
    if not st.session_state.rag_chain:
        st.error("System not initialized.")
        return False
    session = get_current_session()
    if not session:
        create_new_chat()
        session = get_current_session()
    with st.spinner("🔍 Searching legal documents..."):
        result = st.session_state.rag_chain.query(query_text.strip())
        answer = result["answer"]
        sources = result.get("source_documents", [])
        add_to_session(session["id"], query_text.strip(), answer, sources)
    return True


def render_help_page():
    """Render Help/FAQ Page with pagination"""
    help_items = [
        {
            "title": "❓ How do I ask a legal question?",
            "description": "Simply type your legal question in the chat box at the bottom of the page and press Enter. The AI will search through Indian legal documents and provide relevant information."
        },
        {
            "title": "🎭 What are Scenario Templates?",
            "description": "Scenario templates help you ask 'what-if' questions about legal situations. They provide common legal scenarios in India that you can learn from."
        },
        {
            "title": "📚 Which laws are covered?",
            "description": "NyayaSahayak covers Indian Penal Code (IPC), Bharatiya Nyaya Sanhita (BNS), Code of Criminal Procedure (CrPC), Consumer Protection Act, IT Act, and more."
        },
        {
            "title": "🔍 Can I see source documents?",
            "description": "Yes! Click 'View Source Evidence' under each answer to see the legal documents and specific sections that were used to generate the response."
        },
        {
            "title": "🎤 How do I use voice input?",
            "description": "Enable voice input in the sidebar (if available). Choose your language (English or हिंदी), click the microphone button, and speak your question."
        },
        {
            "title": "💾 How is my chat history saved?",
            "description": "Your chat history is automatically saved locally on your device. You can view previous conversations in the 'Chat History' section of the sidebar."
        },
        {
            "title": "⚖️ Is this legal advice?",
            "description": "No. NyayaSahayak is for educational purposes only. It simplifies legal concepts but is NOT a substitute for professional legal counsel. Always consult a lawyer for actual legal matters."
        },
        {
            "title": "🔐 Is my data secure?",
            "description": "Your data is processed locally. Chat histories are stored on your device. We do not upload your questions to external servers."
        }
    ]
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">❓ Help & Frequently Asked Questions</div>
        <div class="page-subtitle">Everything you need to know about NyayaSahayak</div>
    </div>
    """, unsafe_allow_html=True)
    
    paginated_items, total_pages = paginate_items(help_items, st.session_state.help_page, items_per_page=3)
    
    for item in paginated_items:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">{item['title']}</div>
            <div>{item['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    render_pagination(st.session_state.help_page, total_pages, "help_page")


def render_about_page():
    """Render About Page with pagination"""
    about_sections = [
        {
            "title": "🏛️ What is NyayaSahayak?",
            "description": "NyayaSahayak means 'Legal Helper' in Sanskrit. It's an AI-powered legal assistant designed specifically for Indian laws, making legal information accessible to everyone."
        },
        {
            "title": "🎯 Our Mission",
            "description": "To democratize legal knowledge in India by providing instant access to information about Indian laws in a simple, understandable format. We believe everyone deserves to understand their legal rights."
        },
        {
            "title": "🔬 How does it work?",
            "description": "NyayaSahayak uses Retrieval-Augmented Generation (RAG) technology. When you ask a question, it searches a database of Indian legal documents and uses AI to generate an accurate answer with evidence."
        },
        {
            "title": "📖 Technology Stack",
            "description": "Built with Python, Streamlit, LangChain, FAISS Vector Database, and Google Gemini AI. Open-source and designed for educational purposes."
        },
        {
            "title": "👥 Who built this?",
            "description": "NyayaSahayak was created for the ThinkX Hackathon. Our team of developers and legal enthusiasts combined their passion for technology and justice."
        },
        {
            "title": "⚠️ Important Disclaimer",
            "description": "NyayaSahayak is NOT a licensed legal service provider. Information provided is for educational purposes. Always consult a qualified lawyer for legal advice. We are not responsible for any decisions made based on this tool."
        },
        {
            "title": "🌍 Open Source",
            "description": "NyayaSahayak is built with open-source technologies. We're committed to transparency and community contribution."
        },
        {
            "title": "📞 Contact & Support",
            "description": "For feedback, bug reports, or suggestions, please reach out to our team. Your input helps us improve the platform for everyone in India."
        }
    ]
    
    st.markdown("""
    <div class="page-header">
        <div class="page-title">ℹ️ About NyayaSahayak</div>
        <div class="page-subtitle">Your AI-Powered Legal Assistant for Indian Laws</div>
    </div>
    """, unsafe_allow_html=True)
    
    paginated_items, total_pages = paginate_items(about_sections, st.session_state.about_page, items_per_page=3)
    
    for item in paginated_items:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">{item['title']}</div>
            <div>{item['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    render_pagination(st.session_state.about_page, total_pages, "about_page")


def render_civil_criminal_page():
    """Render Interactive Civil vs Criminal Case Comparison Tool"""
    
    # Enhanced CSS for better UI
    st.markdown("""
    <style>
    /* Civil vs Criminal Page Styles */
    .cc-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .cc-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .cc-header-content {
        position: relative;
        z-index: 2;
    }
    .cc-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .cc-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Input Section */
    .cc-input-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .cc-input-label {
        color: #667eea;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    /* Results Container */
    .cc-results {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    /* Comparison Cards */
    .cc-comparison-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    .cc-comparison-card.civil {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);
    }
    .cc-comparison-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .cc-comparison-content {
        font-size: 0.95rem;
        line-height: 1.8;
        opacity: 0.95;
    }
    
    /* Info Cards with Icons */
    .cc-info-card {
        background: white;
        border-left: 5px solid #667eea;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .cc-info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        border-left-color: #f5576c;
    }
    .cc-info-card.civil {
        border-left-color: #f5576c;
    }
    .cc-info-title {
        font-weight: 700;
        color: #667eea;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .cc-info-card.civil .cc-info-title {
        color: #f5576c;
    }
    
    /* Tab Navigation */
    .cc-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 1rem;
    }
    .cc-tab-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        border: 2px solid transparent;
        background: #f1f5f9;
        color: #475569;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .cc-tab-btn:hover {
        background: #e2e8f0;
    }
    .cc-tab-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .cc-results {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .cc-title {
            font-size: 1.8rem;
        }
        .cc-subtitle {
            font-size: 0.9rem;
        }
        .cc-header {
            padding: 2rem 1rem;
        }
        .cc-input-container {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="cc-header">
        <div class="cc-header-content">
            <div class="cc-title">⚖️ Civil vs Criminal Cases</div>
            <div class="cc-subtitle">Interactive Guide - Ask Questions & Get Detailed Comparisons</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for this page
    if "cc_user_query" not in st.session_state:
        st.session_state.cc_user_query = ""
    if "cc_response" not in st.session_state:
        st.session_state.cc_response = None
    if "cc_mode" not in st.session_state:
        st.session_state.cc_mode = "ask"
    
    # Mode Selector
    st.markdown("### 🎯 Choose Your Path")
    mode_cols = st.columns(3)
    with mode_cols[0]:
        if st.button("💬 Ask a Question", use_container_width=True, key="cc_mode_ask"):
            st.session_state.cc_mode = "ask"
            st.rerun()
    with mode_cols[1]:
        if st.button("📊 Quick Comparison", use_container_width=True, key="cc_mode_compare"):
            st.session_state.cc_mode = "compare"
            st.rerun()
    with mode_cols[2]:
        if st.button("🔍 Scenario Analysis", use_container_width=True, key="cc_mode_scenario"):
            st.session_state.cc_mode = "scenario"
            st.rerun()
    
    st.markdown("---")
    
    # MODE 1: ASK A QUESTION (DYNAMIC - Uses RAG)
    if st.session_state.cc_mode == "ask":
        st.markdown("""
        <div class="cc-input-container">
            <div class="cc-input-label">📝 Ask About Civil or Criminal Cases</div>
            <span style="font-size: 0.9rem; color: #64748b;">Examples: "What happens if I breach a contract?", "Difference between theft and robbery?", "What's the punishment for cheating?"</span>
        </div>
        """, unsafe_allow_html=True)
        
        user_query = st.text_area(
            "Your question:",
            placeholder="Type your question about civil or criminal cases here...",
            height=100,
            key="cc_query_input",
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            process_btn = st.button("🔍 Get Answer from Legal Documents", use_container_width=True, key="cc_process_query")
        with col2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True, key="cc_clear_query")
        
        if clear_btn:
            st.session_state.cc_query_input = ""
            st.session_state.cc_response = None
            st.rerun()
        
        if process_btn and user_query.strip():
            if st.session_state.rag_chain:
                with st.spinner("🔍 Searching legal documents..."):
                    # Query the RAG system for answer
                    result = st.session_state.rag_chain.query(user_query.strip())
                    st.session_state.cc_response = {
                        "query": user_query.strip(),
                        "answer": result["answer"],
                        "sources": result.get("source_documents", [])
                    }
            else:
                st.error("RAG system not initialized. Please go to Chat and initialize first.")
        
        # Display Response
        if st.session_state.cc_response:
            st.markdown("""
            <div id="ask-results-anchor"></div>
            <div class="cc-results">
                <div style="font-size: 1.2rem; font-weight: 700; color: #667eea; margin-bottom: 1rem;">
                    📋 Legal Analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-scroll to results
            components.html("""
            <script>
                setTimeout(function() {
                    window.parent.document.getElementById('ask-results-anchor').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 200);
            </script>
            """, height=0)
            
            # Answer Cards
            st.markdown(f"""
            <div class="cc-info-card">
                <div class="cc-info-title">❓ Your Question</div>
                <div style="color: #475569; font-size: 0.95rem;">{st.session_state.cc_response['query']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            answer_text = st.session_state.cc_response['answer']
            
            # Parse and render answer with styling
            st.markdown(f"""
            <div class="cc-info-card">
                <div class="cc-info-title">✅ Answer</div>
                <div style="color: #475569; font-size: 0.95rem; line-height: 1.8;">
                    {answer_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Source Evidence
            sources = st.session_state.cc_response.get('sources', [])
            if sources:
                with st.expander("📚 Source Documents (Legal References)", expanded=False):
                    for i, doc in enumerate(sources[:4], 1):
                        source_name = doc.metadata.get("source", "Legal Document")
                        content_preview = doc.page_content[:250]
                        st.markdown(f"""
                        <div class="cc-info-card" style="border-left-color: #3b82f6;">
                            <div class="cc-info-title">📄 Source {i}</div>
                            <div><strong>{source_name}</strong></div>
                            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">{content_preview}...</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Legal terms explainer
            render_jargon_explainer(answer_text)
            
            st.markdown("---")
            
            # Related Actions
            st.markdown("### 🔗 Related Questions")
            related_questions = [
                "What is the difference between civil and criminal cases?",
                "What are my rights in a criminal case?",
                "What remedies are available in civil disputes?",
                "What is the burden of proof in each type of case?"
            ]
            
            cols = st.columns(2)
            for idx, related_q in enumerate(related_questions):
                with cols[idx % 2]:
                    if st.button(f"❓ {related_q[:40]}...", use_container_width=True, key=f"related_{idx}"):
                        st.session_state.cc_query_input = related_q
                        st.rerun()
    
    # MODE 2: QUICK COMPARISON (DYNAMIC)
    elif st.session_state.cc_mode == "compare":
        st.markdown("""
        <div class="cc-input-container">
            <div class="cc-input-label">📊 Compare Legal Concepts</div>
            <span style="font-size: 0.9rem; color: #64748b;">Enter two legal terms, offenses, or concepts to compare them</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if there are pending values from quick compare buttons
        default_term1 = st.session_state.get("pending_term1", "")
        default_term2 = st.session_state.get("pending_term2", "")
        
        # Clear pending values after reading
        if "pending_term1" in st.session_state:
            del st.session_state.pending_term1
        if "pending_term2" in st.session_state:
            del st.session_state.pending_term2
        
        col1, col2 = st.columns(2)
        with col1:
            term1 = st.text_input("First Term/Concept", value=default_term1, placeholder="e.g., Theft, Murder, Breach of Contract", key="compare_term1")
        with col2:
            term2 = st.text_input("Second Term/Concept", value=default_term2, placeholder="e.g., Robbery, Culpable Homicide, Tort", key="compare_term2")
        
        # Quick comparison suggestions
        st.markdown("**Quick Comparisons:**")
        quick_compare_options = [
            ("Theft vs Robbery", "theft", "robbery"),
            ("Murder vs Culpable Homicide", "murder", "culpable homicide"),
            ("Civil Case vs Criminal Case", "civil case", "criminal case"),
            ("IPC vs BNS", "Indian Penal Code IPC", "Bharatiya Nyaya Sanhita BNS"),
            ("Cheating vs Fraud", "cheating under IPC", "fraud"),
            ("Assault vs Battery", "assault", "battery"),
        ]
        
        qc_cols = st.columns(3)
        for idx, (label, t1, t2) in enumerate(quick_compare_options):
            with qc_cols[idx % 3]:
                if st.button(label, key=f"qc_{idx}", use_container_width=True):
                    st.session_state.pending_term1 = t1
                    st.session_state.pending_term2 = t2
                    st.rerun()
        
        st.markdown("---")
        
        if st.button("🔍 Compare Now", use_container_width=True, type="primary", key="compare_btn"):
            if term1.strip() and term2.strip():
                if st.session_state.rag_chain:
                    with st.spinner("🔍 Analyzing and comparing..."):
                        compare_query = f"""Compare {term1} vs {term2} under Indian law. Provide the comparison in a STRICT TABLE FORMAT.

Format your response EXACTLY like this:

| Aspect | {term1} | {term2} |
|--------|---------|---------|
| Definition | [definition] | [definition] |
| IPC/BNS Section | [section numbers] | [section numbers] |
| Punishment | [punishment details] | [punishment details] |
| Nature | [civil/criminal/both] | [civil/criminal/both] |
| Key Elements | [elements] | [elements] |
| Real Example | [example] | [example] |
| Severity | [severity level] | [severity level] |

After the table, provide a brief SUMMARY (2-3 lines) and KEY DIFFERENCES as bullet points."""
                        
                        result = st.session_state.rag_chain.query(compare_query)
                        st.session_state.cc_response = {
                            "query": f"Compare: {term1} vs {term2}",
                            "answer": result["answer"],
                            "sources": result.get("source_documents", []),
                            "type": "comparison",
                            "term1": term1,
                            "term2": term2
                        }
                else:
                    st.error("⚠️ RAG system not initialized. Please go to Chat and initialize first.")
            else:
                st.warning("Please enter both terms to compare.")
        
        # Show comparison results
        if st.session_state.cc_response and st.session_state.cc_response.get("type") == "comparison":
            resp = st.session_state.cc_response
            
            st.markdown(f"""
            <div id="comparison-results-anchor"></div>
            <div class="cc-results">
                <div style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 1.5rem; text-align: center;">
                    📊 {resp['term1']} vs {resp['term2']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-scroll to results
            components.html("""
            <script>
                setTimeout(function() {
                    window.parent.document.getElementById('comparison-results-anchor').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 200);
            </script>
            """, height=0)
            
            # Custom CSS for comparison table
            st.markdown("""
            <style>
            .comparison-table-container {
                background: #ffffff;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                border: 1px solid #e2e8f0;
                overflow-x: auto;
            }
            .comparison-table-container table {
                width: 100%;
                border-collapse: collapse;
                font-size: 0.9rem;
            }
            .comparison-table-container th {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 0.75rem 1rem;
                text-align: left;
                font-weight: 600;
                border: 1px solid #5a67d8;
            }
            .comparison-table-container td {
                padding: 0.75rem 1rem;
                border: 1px solid #e2e8f0;
                color: #475569;
                vertical-align: top;
            }
            .comparison-table-container tr:nth-child(even) {
                background: #f8fafc;
            }
            .comparison-table-container tr:hover {
                background: #eff6ff;
            }
            .comparison-summary {
                background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
                border-left: 4px solid #667eea;
                padding: 1rem 1.25rem;
                border-radius: 0 8px 8px 0;
                margin-top: 1rem;
            }
            .comparison-summary h4 {
                color: #1e40af;
                margin-bottom: 0.5rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display comparison in markdown (which renders tables nicely)
            st.markdown("### 📋 Detailed Comparison")
            st.markdown(resp['answer'])
            
            # Sources
            sources = resp.get('sources', [])
            if sources:
                with st.expander("📚 Legal References", expanded=False):
                    for i, doc in enumerate(sources[:4], 1):
                        source_name = doc.metadata.get("source", "Legal Document")
                        content_preview = doc.page_content[:200]
                        st.markdown(f"**Source {i}:** {source_name}")
                        st.caption(f"{content_preview}...")
            
            # Legal terms explainer
            render_jargon_explainer(resp['answer'])
        
        # Also show static quick reference
        with st.expander("📖 Quick Reference: Civil vs Criminal Basics", expanded=False):
            aspects = [
                ("👤 Parties", "State vs Accused", "Plaintiff vs Defendant"),
                ("⚖️ Burden of Proof", "Beyond Reasonable Doubt", "Preponderance of Evidence"),
                ("🎯 Purpose", "Punishment", "Compensation"),
                ("💼 Law Used", "CrPC", "CPC"),
            ]
            for aspect, criminal, civil in aspects:
                st.markdown(f"**{aspect}:** Criminal: {criminal} | Civil: {civil}")
    
    # MODE 3: SCENARIO ANALYSIS (FULLY DYNAMIC)
    elif st.session_state.cc_mode == "scenario":
        st.markdown("""
        <div class="cc-input-container">
            <div class="cc-input-label">💡 Try These Sample Scenarios</div>
            <span style="font-size: 0.9rem; color: #64748b;">Click on any scenario below to see a detailed legal analysis</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample scenarios FIRST
        sample_scenarios = [
            {
                "title": "🛡️ Self-Defense Killing",
                "query": "I killed someone who attacked me with a knife. I acted in self-defense but then I fled from the scene because I was scared. What will happen to me legally?"
            },
            {
                "title": "💔 Domestic Violence",
                "query": "My husband beats me regularly. Last night he hit me so hard I had to go to hospital. What legal options do I have to protect myself?"
            },
            {
                "title": "💰 Online Fraud",
                "query": "I paid 50,000 rupees for a phone online but received a brick. The seller blocked me. What can I do legally?"
            },
            {
                "title": "🚗 Hit and Run",
                "query": "I accidentally hit a person with my car. I panicked and drove away. Later I came to know the person died. What punishment will I face?"
            },
            {
                "title": "🏠 Land Encroachment",
                "query": "My neighbor has built a wall 2 feet into my property. He refuses to remove it. How can I get my land back legally?"
            },
            {
                "title": "📱 Cyber Harassment",
                "query": "Someone is sending me threatening messages on social media and sharing my private photos. What legal action can I take?"
            },
        ]
        
        scenario_cols = st.columns(2)
        for idx, scenario in enumerate(sample_scenarios):
            with scenario_cols[idx % 2]:
                st.markdown(f"""
                <div class="cc-info-card" style="border-left-color: #764ba2; padding: 1rem;">
                    <div style="font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">{scenario['title']}</div>
                    <div style="color: #64748b; font-size: 0.85rem;">{scenario['query'][:80]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Analyze This", key=f"sample_scenario_{idx}", use_container_width=True):
                    if st.session_state.rag_chain:
                        with st.spinner("🔍 Analyzing scenario..."):
                            scenario_prompt = f"""Analyze this legal situation under Indian law:

SITUATION: {scenario['query']}

Please provide:
1. Is this a civil case, criminal case, or both?
2. What specific laws/sections apply (IPC/BNS, CrPC, etc.)?
3. What are the possible consequences/punishments?
4. What are the legal rights and options?
5. What defenses might be available?
6. What steps should be taken now?

Be specific and cite relevant sections of Indian law."""
                            
                            result = st.session_state.rag_chain.query(scenario_prompt)
                            st.session_state.cc_response = {
                                "query": scenario['query'],
                                "answer": result["answer"],
                                "sources": result.get("source_documents", []),
                                "type": "scenario_analysis"
                            }
                            st.rerun()
                    else:
                        st.error("RAG not initialized. Go to Chat first.")
        
        st.markdown("---")
        
        # Custom scenario input AFTER samples
        st.markdown("""
        <div class="cc-input-container">
            <div class="cc-input-label">🎭 Or Describe Your Own Situation</div>
            <span style="font-size: 0.9rem; color: #64748b;">Tell us what happened in your own words. We'll analyze the legal implications.</span>
        </div>
        """, unsafe_allow_html=True)
        
        custom_scenario = st.text_area(
            "Describe your situation:",
            placeholder="Example: I killed someone in self-defense and then fled from that place. What will happen to me? What are my legal options?\n\nOr: My neighbor has encroached on my land and refuses to leave. What can I do?\n\nOr: I was cheated by an online seller who took my money but never delivered the product.",
            height=150,
            key="custom_scenario_input",
            label_visibility="collapsed"
        )
        
        analyze_col1, analyze_col2 = st.columns([3, 1])
        with analyze_col1:
            analyze_btn = st.button("🔍 Analyze My Scenario", use_container_width=True, type="primary", key="analyze_scenario_btn")
        with analyze_col2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True, key="clear_scenario_btn")
        
        if clear_btn:
            st.session_state.custom_scenario_input = ""
            st.session_state.cc_response = None
            st.rerun()
        
        if analyze_btn and custom_scenario.strip():
            if st.session_state.rag_chain:
                with st.spinner("🔍 Analyzing your scenario under Indian law..."):
                    scenario_query = f"""Analyze this legal situation under Indian law:

SITUATION: {custom_scenario.strip()}

Please provide:
1. Is this a civil case, criminal case, or both?
2. What specific laws/sections apply to this situation (IPC/BNS, CrPC, etc.)?
3. What are the possible consequences/punishments?
4. What are my legal rights and options?
5. What defenses might be available?
6. What steps should I take now?
7. Do I need a lawyer? What kind?

Be specific and cite relevant sections of Indian law."""
                    
                    result = st.session_state.rag_chain.query(scenario_query)
                    st.session_state.cc_response = {
                        "query": custom_scenario.strip(),
                        "answer": result["answer"],
                        "sources": result.get("source_documents", []),
                        "type": "scenario_analysis"
                    }
            else:
                st.error("⚠️ RAG system not initialized. Please go to Chat and initialize first.")
        
        # Display scenario analysis results
        if st.session_state.cc_response and st.session_state.cc_response.get("type") == "scenario_analysis":
            resp = st.session_state.cc_response
            
            # Anchor and auto-scroll to results
            st.markdown("""
            <div id="scenario-results-anchor"></div>
            <div class="cc-results">
                <div style="font-size: 1.3rem; font-weight: 700; color: #764ba2; margin-bottom: 1rem;">
                    🔍 Legal Analysis of Your Situation
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-scroll to results
            components.html("""
            <script>
                setTimeout(function() {
                    window.parent.document.getElementById('scenario-results-anchor').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 200);
            </script>
            """, height=0)
            
            # Show user's scenario
            st.markdown(f"""
            <div class="cc-info-card" style="border-left-color: #f5576c;">
                <div class="cc-info-title" style="color: #f5576c;">📝 Your Situation</div>
                <div style="color: #475569; font-size: 0.95rem; font-style: italic;">"{resp['query']}"</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show analysis
            st.markdown(f"""
            <div class="cc-info-card" style="border-left-color: #667eea;">
                <div class="cc-info-title">⚖️ Legal Analysis</div>
                <div style="color: #475569; font-size: 0.95rem; line-height: 1.9; white-space: pre-wrap;">
{resp['answer']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sources
            sources = resp.get('sources', [])
            if sources:
                with st.expander("📚 Legal References Used", expanded=False):
                    for i, doc in enumerate(sources[:4], 1):
                        source_name = doc.metadata.get("source", "Legal Document")
                        content_preview = doc.page_content[:250]
                        st.markdown(f"**📄 Source {i}:** {source_name}")
                        st.caption(f"{content_preview}...")
            
            # Legal terms explanation
            render_jargon_explainer(resp['answer'])
            
            # Warning disclaimer
            st.warning("⚠️ **Disclaimer:** This analysis is for informational purposes only and does not constitute legal advice. Please consult a qualified lawyer for your specific situation.")

def main():
    """Main application"""
    
    # ============== AUTHENTICATION CHECK ==============
    AuthManager.init_session()
    
    if not AuthManager.is_authenticated():
        render_auth_page()
        return
    
    # Get current user
    user = AuthManager.get_current_user()
    
    # Premium Sidebar Navigation
    with st.sidebar:
        # User Info Section
        st.markdown(f"""
        <div style="background: #eff6ff; border-left: 4px solid #2563eb; padding: 0.75rem 1rem; 
                    border-radius: 0 8px 8px 0; margin-bottom: 1rem;">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; font-weight: 600;">Logged in as</div>
            <div style="font-weight: 600; color: #1e293b; font-size: 0.95rem; margin-top: 0.25rem;">{user['name'] if user else 'User'}</div>
            <div style="font-size: 0.75rem; color: #64748b;">{user['email'] if user else ''}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            AuthManager.logout()
            st.rerun()
        
        st.markdown("---")
        
        # Logo/Brand Section
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.25rem;">⚖️</div>
            <div style="font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.1rem; 
                        color: #1e293b;">NyayaSahayak</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.15rem;">AI Legal Assistant</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Buttons - Premium Style
        st.markdown("### 🧭 Navigate")
        
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("💬 Chat", use_container_width=True, key="page_chat"):
                st.session_state.current_page = "chat"
                st.rerun()
            if st.button("❓ Help", use_container_width=True, key="page_help"):
                st.session_state.current_page = "help"
                st.rerun()
        with nav_col2:
            if st.button("⚖️ Cases", use_container_width=True, key="page_civil_criminal"):
                st.session_state.current_page = "civil_criminal"
                st.rerun()
            if st.button("ℹ️ About", use_container_width=True, key="page_about"):
                st.session_state.current_page = "about"
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.current_page == "chat":
            # Chat Controls
            st.markdown("### ⚡ Quick Actions")
            ctrl_col1, ctrl_col2 = st.columns(2)
            with ctrl_col1:
                if st.button("➕ New", use_container_width=True, type="primary"):
                    create_new_chat()
                    st.session_state.pending_query = None
                    st.rerun()
            with ctrl_col2:
                if st.button("🗑️ Clear", use_container_width=True):
                    clear_current_chat()
                    st.rerun()

            # Chat History
            st.markdown("### 📜 History")
            sessions = load_chat_sessions()
            if sessions:
                for s in sessions[:8]:  # Limit to 8 recent chats
                    is_active = s["id"] == st.session_state.current_session_id
                    btn_label = f"{'⚡ ' if is_active else '○ '}{s['title'][:25]}{'...' if len(s['title']) > 25 else ''}"
                    if st.button(btn_label, key=f"hist_{s['id']}", use_container_width=True):
                        st.session_state.current_session_id = s["id"]
                        st.rerun()
            else:
                st.caption("No conversations yet")

            st.markdown("---")
            
            # Language & Voice Settings - Clean Design
            if MULTILINGUAL_AVAILABLE:
                try:
                    from frontend.multilingual_ui import MultilingualUI
                    from backend.multilingual import INDIAN_LANGUAGES
                    multilingual_ui = MultilingualUI()
                    
                    # Language Settings Card
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%); 
                                border-radius: 12px; padding: 1rem; margin-bottom: 1rem;
                                border: 1px solid #dbeafe;">
                        <div style="font-size: 0.9rem; font-weight: 700; color: #1e40af; margin-bottom: 0.75rem; display: flex; align-items: center;">
                            🌍 Language Settings
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interface Language
                    all_langs = list(INDIAN_LANGUAGES.keys())
                    current_lang = st.session_state.get('user_language', 'english')
                    current_idx = all_langs.index(current_lang) if current_lang in all_langs else 0
                    
                    selected_lang = st.selectbox(
                        "🗣️ Interface Language",
                        options=all_langs,
                        format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                        index=current_idx,
                        key="sidebar_interface_lang",
                        help="Choose language for the interface"
                    )
                    if selected_lang != current_lang:
                        st.session_state.user_language = selected_lang
                        st.rerun()
                    
                    # Response Language
                    current_resp_lang = st.session_state.get('response_language', 'english')
                    current_resp_idx = all_langs.index(current_resp_lang) if current_resp_lang in all_langs else 0
                    
                    response_lang = st.selectbox(
                        "💬 Response Language",
                        options=all_langs,
                        format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                        index=current_resp_idx,
                        key="sidebar_response_lang",
                        help="Get AI responses in this language"
                    )
                    if response_lang != current_resp_lang:
                        st.session_state.response_language = response_lang
                        st.rerun()
                    
                    # Voice Input Section
                    if VOICE_AVAILABLE:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%); 
                                    border-radius: 12px; padding: 1rem; margin: 1rem 0;
                                    border: 1px solid #fcd34d;">
                            <div style="font-size: 0.9rem; font-weight: 700; color: #92400e; margin-bottom: 0.5rem;">
                                🎤 Voice Input
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Voice language selection - ALL languages from dropdown
                        current_voice_lang = st.session_state.get('voice_language', 'english')
                        voice_lang_idx = all_langs.index(current_voice_lang) if current_voice_lang in all_langs else 0
                        
                        voice_lang_selected = st.selectbox(
                            "🗣️ Speak in:",
                            options=all_langs,
                            format_func=lambda x: f"{INDIAN_LANGUAGES[x]['flag']} {INDIAN_LANGUAGES[x]['name']}",
                            index=voice_lang_idx,
                            key="sidebar_voice_lang",
                            help="Choose your voice input language"
                        )
                        
                        if voice_lang_selected != current_voice_lang:
                            st.session_state.voice_language = voice_lang_selected
                        
                        # Get voice code for selected language
                        voice_code = INDIAN_LANGUAGES[voice_lang_selected]['voice_code']
                        
                        # Microphone button
                        voice_text = speech_to_text(
                            language=voice_code,
                            start_prompt="🎤 Click to Speak",
                            stop_prompt="⏹️ Stop Recording",
                            just_once=True,
                            use_container_width=True,
                            key="sidebar_voice_stt"
                        )
                        if voice_text:
                            st.session_state.pending_query = voice_text
                            st.rerun()
                    
                    st.markdown("---")
                    
                    # Emergency Contacts Compact
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%); 
                                border-radius: 12px; padding: 0.75rem; 
                                border: 1px solid rgba(239, 68, 68, 0.2);">
                        <div style="font-size: 0.85rem; font-weight: 600; color: #dc2626; margin-bottom: 0.5rem;">🚨 Emergency Helplines</div>
                        <div style="font-size: 0.75rem; color: #1f2937; line-height: 1.6;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                <span>👮 Police</span><strong>100</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                                <span>👩 Women Helpline</span><strong>181</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span>⚖️ Legal Aid</span><strong>15100</strong>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    # Fallback to basic voice input
                    if VOICE_AVAILABLE:
                        st.markdown("### 🎤 Voice Input")
                        voice_lang = st.radio("Language:", ["English", "हिंदी"], 
                                             index=0 if st.session_state.voice_lang == "en" else 1,
                                             key="voice_lang_radio", horizontal=True)
                        st.session_state.voice_lang = "en" if "English" in voice_lang else "hi"
                        voice_text = speech_to_text(
                            language=st.session_state.voice_lang,
                            start_prompt="🎤 Speak",
                            stop_prompt="⏹️ Stop",
                            just_once=True,
                            use_container_width=True,
                            key="voice_stt"
                        )
                        if voice_text:
                            st.session_state.pending_query = voice_text
                            st.rerun()
            elif VOICE_AVAILABLE:
                st.markdown("### 🎤 Voice")
                voice_lang = st.radio("Language:", ["English", "हिंदी"],
                                     index=0 if st.session_state.voice_lang == "en" else 1,
                                     key="voice_lang_basic", horizontal=True)
                st.session_state.voice_lang = "en" if "English" in voice_lang else "hi"
                voice_text = speech_to_text(
                    language=st.session_state.voice_lang,
                    start_prompt="🎤 Speak",
                    stop_prompt="⏹️ Stop",
                    just_once=True,
                    use_container_width=True,
                    key="voice_stt_basic"
                )
                if voice_text:
                    st.session_state.pending_query = voice_text
                    st.rerun()
                
                # Emergency Contacts for non-multilingual fallback
                st.markdown("---")
                st.markdown("""
                <div style="background: rgba(239, 68, 68, 0.1); border-radius: 12px; padding: 0.75rem; border: 1px solid rgba(239, 68, 68, 0.2);">
                    <div style="font-size: 0.85rem; font-weight: 600; color: #ef4444; margin-bottom: 0.5rem;">🚨 Emergency</div>
                    <div style="font-size: 0.75rem; color: #1f2937; line-height: 1.6;">
                        Police: <b>100</b> • Women: <b>181</b><br>Legal Aid: <b>15100</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("---")
            st.caption("💡 Select a page above to navigate")
        
        # Footer
        st.markdown("---")
        st.caption("⚠️ For education only. Consult a lawyer for legal advice.")

    # Page Content Display
    if st.session_state.current_page == "help":
        render_help_page()
        return
    elif st.session_state.current_page == "civil_criminal":
        render_civil_criminal_page()
        return
    elif st.session_state.current_page == "about":
        render_about_page()
        return

    # ============== CHAT PAGE ==============
    # Main content
    if not st.session_state.vector_store_initialized:
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">⚖️ Welcome to NyayaSahayak</div>
            <div class="hero-subtitle">AI-Powered Legal Assistant for Indian Laws</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <div style="font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">
                Initialize the system to start asking legal questions
            </div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">
                This will load the legal document database
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if config.GOOGLE_API_KEY and st.button("🚀 Initialize NyayaSahayak", use_container_width=True, type="primary"):
            if initialize_system():
                st.rerun()
        return

    # Ensure current session exists
    get_current_session()

    # ============== Process pending query (from category/voice/surprise) ==============
    if st.session_state.pending_query:
        q = st.session_state.pending_query
        st.session_state.pending_query = None
        if process_query(q):
            st.rerun()

    # ============== Quick Legal Topics - Premium Design ==============
    st.markdown("""
    <div class="sticky-header-container">
        <div class="sticky-title">⚡ Quick Legal Topics</div>
    </div>
    """, unsafe_allow_html=True)

    # Render quick topic buttons in responsive grid
    shuffled_cats = get_shuffled_categories()
    num_cols = min(4, len(shuffled_cats))
    cols = st.columns(num_cols)
    for i, cat in enumerate(shuffled_cats[:8]):
        with cols[i % num_cols]:
            if st.button(f"{cat['icon']} {cat['title']}", key=f"cat_{cat['id']}_{i}", use_container_width=True, help=cat['desc']):
                st.session_state.pending_query = cat["query"]
                st.rerun()
    
    # Action buttons row
    action_cols = st.columns([1, 1, 2])
    with action_cols[0]:
        if st.button("✨ Surprise", use_container_width=True, key="surprise_me"):
            all_queries = [c["query"] for c in LEGAL_CATEGORIES] + get_shuffled_scenarios()
            st.session_state.pending_query = random.choice(all_queries)
            st.rerun()
    with action_cols[1]:
        if st.button("🔄 Shuffle", use_container_width=True, key="refresh_topics"):
            st.session_state.card_shuffle_seed = random.randint(0, 99999)
            st.rerun()

    st.markdown("---")

    # ============== Chat Display ==============
    messages = get_session_messages(st.session_state.current_session_id or "") if st.session_state.current_session_id else []
    
    # Show hero section only if no messages
    if not messages:
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">⚖️ How can I help you?</div>
            <div class="hero-subtitle">Ask anything about Indian Laws • BNS • IPC • CrPC • Consumer Protection & More</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggestion cards
        st.markdown("### 💡 Try asking about...")
        suggestion_cols = st.columns(2)
        suggestions = [
            ("🚔", "What are my rights during arrest?"),
            ("💰", "What is punishment for cheating under IPC 420?"),
            ("🛡️", "How to file a consumer complaint?"),
            ("👩", "What protection do women have against harassment?"),
        ]
        for idx, (icon, suggestion) in enumerate(suggestions):
            with suggestion_cols[idx % 2]:
                if st.button(f"{icon} {suggestion}", key=f"suggest_{idx}", use_container_width=True):
                    st.session_state.pending_query = suggestion
                    st.rerun()
    else:
        st.markdown("### 💬 Conversation")
    
    # Messages display
    for i, (q, a, sources) in enumerate(messages):
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            render_answer_cards(a)
            render_jargon_explainer(a)
            with st.expander("📎 View Source Evidence", expanded=(i == len(messages) - 1)):
                render_source_cards(sources)

    # Auto-scroll to bottom when messages exist - keeps newest visible, older msgs scroll up
    if messages:
        st.markdown('<div id="chat-bottom-anchor"></div>', unsafe_allow_html=True)
        try:
            import streamlit.components.v1 as components
            components.html("""
            <script>
            (function(){
                function scrollToBottom() {
                    try {
                        var p = window.parent;
                        var container = p.document.querySelector('[data-testid="stAppViewContainer"]');
                        if (container) {
                            container.scrollTop = container.scrollHeight;
                        }
                        var body = p.document.body;
                        if (body) body.scrollTop = body.scrollHeight;
                        if (p.document.documentElement) p.document.documentElement.scrollTop = p.document.documentElement.scrollHeight;
                    } catch(e) {}
                }
                scrollToBottom();
                setTimeout(scrollToBottom, 100);
                setTimeout(scrollToBottom, 300);
            })();
            </script>
            """, height=0)
        except Exception:
            pass

    # ============== Chat Input at Bottom (ChatGPT Style) ==============
    st.markdown("---")
    chat_msg = st.chat_input("Type your question and press **Enter** to search...")
    if chat_msg:
        if process_query(chat_msg):
            st.rerun()

    st.caption("💡 Press **Enter** to send • Your questions are processed through legal documents")

    # Dynamic Scenario templates with pagination
    if st.session_state.query_mode == "scenario" and not messages:
        st.markdown("### 🎭 Scenario Templates")
        all_scenarios = get_shuffled_scenarios()
        paginated_scenarios, total_pages = paginate_items(all_scenarios, st.session_state.scenario_page, items_per_page=4)
        
        scenario_cols = st.columns(2)
        for i, scenario in enumerate(paginated_scenarios):
            with scenario_cols[i % 2]:
                btn_text = (scenario[:45] + "…") if len(scenario) > 45 else scenario
                if st.button(btn_text, key=f"scenario_{i}", use_container_width=True):
                    st.session_state.pending_query = scenario
                    st.rerun()
        
        st.markdown("---")
        render_pagination(st.session_state.scenario_page, total_pages, "scenario_page")

    # Extra: Download current chat as text
    if messages:
        st.markdown("---")
        chat_text = ""
        for q, a, _ in messages:
            chat_text += f"Q: {q}\n\nA: {a}\n\n---\n\n"
        st.download_button("📥 Download This Chat", chat_text, file_name="legal_chat.txt", mime="text/plain", use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("NyayaSahayak • Built for hackathon • Not a substitute for professional legal counsel")


if __name__ == "__main__":
    main()
