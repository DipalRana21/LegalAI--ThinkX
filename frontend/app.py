"""
NyayaSahayak - LLM-based Intelligent Legal Assistance System for Indian Laws
Streamlit Frontend - Modern, Stylish, Feature-Rich
"""

import streamlit as st
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

# Page configuration
st.set_page_config(
    page_title="NyayaSahayak - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== MODERN UI - Indian Legal Theme (Navy + Saffron + Gold) ==============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --navy: #0f3460;
    --navy-light: #1a4a7a;
    --saffron: #f59e0b;
    --saffron-light: #fbbf24;
    --gold: #d4af37;
    --cream: #fef3c7;
    --white: #ffffff;
    --gray-100: #f8fafc;
    --gray-200: #e2e8f0;
    --gray-600: #475569;
}

/* Main container */
.main .block-container {
    padding: 2rem 3rem;
    max-width: 1200px;
}

/* Hero Section */
.hero-section {
    background: linear-gradient(135deg, #0f3460 0%, #1e3a5f 50%, #0f3460 100%);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 25px 50px -12px rgba(15, 52, 96, 0.4);
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #fff 0%, #fbbf24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 400;
}

/* Dynamic Category Cards - Glassmorphism + Animations */
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes cardPulse {
    0%, 100% { box-shadow: 0 4px 15px rgba(15, 52, 96, 0.08); }
    50% { box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2); }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.category-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.9) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 16px;
    padding: 1.25rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(15, 52, 96, 0.08);
    animation: cardFadeIn 0.5s ease-out forwards;
}
.category-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 30px rgba(15, 52, 96, 0.15);
    border-color: #f59e0b;
    animation: cardPulse 2s ease-in-out infinite;
}
.surprise-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
    border-color: #f59e0b !important;
    font-weight: 600 !important;
}
.category-icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}
.category-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: #0f3460;
    font-size: 1rem;
}
.category-desc {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 0.25rem;
}

/* Chat Bubbles */
.user-bubble {
    background: linear-gradient(135deg, #0f3460 0%, #1a4a7a 100%);
    color: white;
    padding: 1rem 1.25rem;
    border-radius: 18px 18px 4px 18px;
    margin: 1rem 0;
    max-width: 85%;
    margin-left: auto;
    box-shadow: 0 4px 15px rgba(15, 52, 96, 0.2);
}
.assistant-bubble {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    color: #1e293b;
    padding: 1.25rem 1.5rem;
    border-radius: 18px 18px 18px 4px;
    margin: 1rem 0;
    border-left: 4px solid #f59e0b;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

/* Source Evidence Card */
.source-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border-left: 4px solid #0f3460;
}
.source-card:hover {
    border-color: #f59e0b;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
}

/* Query Mode Pills */
.mode-pill {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.25rem;
    cursor: pointer;
}
.mode-pill-active {
    background: #0f3460;
    color: white;
}
.mode-pill-inactive {
    background: #f1f5f9;
    color: #64748b;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #0f3460 0%, #1a4a7a 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(15, 52, 96, 0.3) !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #1a4a7a 0%, #0f3460 100%) !important;
    box-shadow: 0 6px 20px rgba(15, 52, 96, 0.4) !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Input styling */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
}
.stTextArea textarea:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
}

/* Chat input - Enter to send hint */
.chat-hint { font-size: 0.8rem; color: #64748b; margin-top: 0.25rem; }

/* Voice button styling */
.voice-section { padding: 0.5rem 0; }

/* Chat flow: messages top-to-bottom, input below messages */
#chat-bottom-anchor { height: 1px; }

/* ChatGPT-style main container */
.main .block-container {
    max-width: 900px;
    margin: 0 auto;
}

/* Sticky header styling for quick topics */
.stButton > button {
    font-size: 0.9rem !important;
}

/* Card-based answer sections */
.answer-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #0f3460;
}
.answer-card.summary { border-left-color: #10b981; }
.answer-card.points { border-left-color: #f59e0b; }
.answer-card.law { border-left-color: #6366f1; }
.answer-card.steps { border-left-color: #ec4899; }
.answer-card-title { font-weight: 600; color: #0f3460; margin-bottom: 0.5rem; font-size: 0.95rem; }
.chat-history-item { padding: 0.5rem; border-radius: 8px; margin: 0.25rem 0; cursor: pointer; }
.chat-history-item:hover { background: #f1f5f9; }
.chat-history-item.active { background: #dbeafe; border-left: 3px solid #0f3460; }

/* Quick Topics Cards - Perfectly Styled */
.quick-topics-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: flex-start;
    margin: 1rem 0;
}
.quick-topic-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(15, 52, 96, 0.06);
    font-weight: 500;
    font-size: 0.9rem;
    color: #0f3460;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.quick-topic-card:hover {
    background: linear-gradient(135deg, #0f3460 0%, #1a4a7a 100%);
    color: white;
    border-color: #f59e0b;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(15, 52, 96, 0.2);
}
.quick-topic-icon {
    font-size: 1.2rem;
}

/* Pagination Styling */
.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.pagination-btn {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: white;
    color: #0f3460;
    cursor: pointer;
    transition: all 0.2s ease;
    font-weight: 500;
}
.pagination-btn:hover {
    background: #0f3460;
    color: white;
    border-color: #0f3460;
}
.pagination-btn.active {
    background: #0f3460;
    color: white;
    border-color: #0f3460;
}
.pagination-info {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0 0.5rem;
}

/* Help/About Pages */
.page-header {
    background: linear-gradient(135deg, #0f3460 0%, #1e3a5f 100%);
    color: white;
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(15, 52, 96, 0.2);
}
.page-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.page-subtitle {
    font-size: 1rem;
    opacity: 0.9;
}
.info-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    padding: 1.25rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.info-card-title {
    font-weight: 600;
    color: #0f3460;
    margin-bottom: 0.5rem;
    font-size: 1.05rem;
}
.scenario-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    padding: 1.25rem;
    margin: 0.75rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
}
.scenario-card:hover {
    transform: translateX(5px);
    box-shadow: 0 6px 16px rgba(245, 158, 11, 0.2);
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


def main():
    """Main application"""
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # Page selector
        page_cols = st.columns(3)
        with page_cols[0]:
            if st.button("💬 Chat", use_container_width=True, key="page_chat"):
                st.session_state.current_page = "chat"
                st.rerun()
        with page_cols[1]:
            if st.button("❓ Help", use_container_width=True, key="page_help"):
                st.session_state.current_page = "help"
                st.rerun()
        with page_cols[2]:
            if st.button("ℹ️ About", use_container_width=True, key="page_about"):
                st.session_state.current_page = "about"
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.current_page == "chat":
            st.markdown("### ⚙️ Controls")
            if st.button("➕ New Chat", use_container_width=True, type="primary"):
                create_new_chat()
                st.session_state.pending_query = None
                st.rerun()
            if st.button("🗑️ Clear This Chat", use_container_width=True):
                clear_current_chat()
                st.rerun()

            st.markdown("### 📜 Chat History")
            sessions = load_chat_sessions()
            if sessions:
                for s in sessions:
                    is_active = s["id"] == st.session_state.current_session_id
                    btn_label = f"{'▶ ' if is_active else ''}{s['title']}"
                    if st.button(btn_label, key=f"hist_{s['id']}", use_container_width=True):
                        st.session_state.current_session_id = s["id"]
                        st.rerun()
            else:
                st.caption("No chats yet")

            st.markdown("---")
            st.markdown("### 📖 Query Mode")
            mode = st.radio(
                "How would you like to ask?",
                ["General Question", "Scenario-Based (What if...)", "Specific Article/Section"],
                label_visibility="collapsed",
                key="query_mode_radio"
            )
            if "Scenario" in mode:
                st.session_state.query_mode = "scenario"
            elif "Article" in mode:
                st.session_state.query_mode = "article"
            else:
                st.session_state.query_mode = "general"

            st.markdown("---")
            if VOICE_AVAILABLE:
                st.markdown("### 🎤 Voice Input")
                voice_lang = st.radio(
                    "Speak in:",
                    ["English", "हिंदी (Hindi)"],
                    index=0 if st.session_state.voice_lang == "en" else 1,
                    key="voice_lang_radio"
                )
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
            st.markdown("---")
            st.markdown("### 📞 Emergency")
            st.info("**Police:** 100\n**Women Helpline:** 181\n**Legal Aid:** 15100")
            st.markdown("---")
            st.caption("⚠️ Educational purposes only. Consult a lawyer for legal advice.")
        else:
            st.markdown("---")
            st.caption("💡 Navigate to Chat, Help, or About sections using the buttons above.")

    # Page Content Display
    if st.session_state.current_page == "help":
        render_help_page()
        return
    elif st.session_state.current_page == "about":
        render_about_page()
        return

    # ============== CHAT PAGE ==============
    # Main content
    if not st.session_state.vector_store_initialized:
        st.info("👈 Click below to initialize the system.")
        if config.GOOGLE_API_KEY and st.button("🚀 Initialize NyayaSahayak"):
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

    # ============== STICKY HEADER - Quick Legal Topics (ChatGPT Style) ==============
    st.markdown("""
    <style>
    .sticky-header-container {
        position: sticky;
        top: 60px;
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        z-index: 999;
        padding: 1.5rem 1rem;
        border-bottom: 2px solid #e2e8f0;
        margin: 0 -1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .sticky-title {
        font-size: 1rem;
        font-weight: 600;
        color: #0f3460;
        margin-bottom: 0.75rem;
    }
    .quick-topics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    </style>
    
    <div class="sticky-header-container">
        <div class="sticky-title">📋 Quick Legal Topics</div>
    </div>
    """, unsafe_allow_html=True)

    # Render quick topic buttons in a compact grid
    shuffled_cats = get_shuffled_categories()
    cols = st.columns(min(8, len(shuffled_cats)))
    for i, cat in enumerate(shuffled_cats):
        with cols[i % 8]:
            if st.button(f"{cat['icon']} {cat['title']}", key=f"cat_{cat['id']}_{i}", use_container_width=True, help=cat['desc']):
                st.session_state.pending_query = cat["query"]
                st.rerun()
    
    # Surprise me + Refresh topics (dynamic)
    col_surprise, col_refresh, col_space = st.columns([1, 1, 6])
    with col_surprise:
        if st.button("✨ Surprise me!", use_container_width=True, key="surprise_me"):
            all_queries = [c["query"] for c in LEGAL_CATEGORIES] + get_shuffled_scenarios()
            st.session_state.pending_query = random.choice(all_queries)
            st.rerun()
    with col_refresh:
        if st.button("🔄 Refresh", use_container_width=True, key="refresh_topics"):
            st.session_state.card_shuffle_seed = random.randint(0, 99999)
            st.rerun()

    st.markdown("---")

    # ============== Chat Display - st.chat_message for normal AI flow (center, ChatGPT style) ==============
    messages = get_session_messages(st.session_state.current_session_id or "") if st.session_state.current_session_id else []
    
    # Show hero section only if no messages (like ChatGPT)
    if not messages:
        st.markdown("""
        <div class="hero-section">
            <div class="hero-title">⚖️ How can I help?</div>
            <div class="hero-subtitle">Ask anything about Indian Laws • BNS, IPC, CrPC, Consumer Protection & More</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 📜 Conversation")
    
    # Messages in st.chat_message - oldest at top, newest at bottom, auto-scrolling handled
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
