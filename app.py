import streamlit as st
import time
from rag import get_answer

# --- 1. PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="NyayaSahayak - Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
<style>
    /* GOOGLE FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
    }

    /* ========== OVERALL PAGE ========== */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1535 50%, #0d0c1d 100%);
        color: #e8eaed;
        overflow-x: hidden;
    }

    html, body {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1535 50%, #0d0c1d 100%);
    }

    /* ========== CHAT MESSAGE STYLING ========== */
    .stChatMessage {
        animation: slideIn 0.4s ease-out;
        background: linear-gradient(135deg, rgba(30, 30, 46, 0.6) 0%, rgba(50, 40, 80, 0.3) 100%);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 14px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stChatMessage:hover {
        background: linear-gradient(135deg, rgba(40, 40, 60, 0.8) 0%, rgba(60, 50, 90, 0.4) 100%);
        border-color: rgba(255, 215, 0, 0.3);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.1);
        transform: translateY(-2px);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ========== CHAT MESSAGE CONTENT ========== */
    .stChatMessage p {
        line-height: 1.7;
        font-size: 15px;
        font-weight: 400;
        color: #e8eaed;
    }

    /* ========== AVATARS ========== */
    .stChatMessage .stChatMessageAvatar {
        background: linear-gradient(135deg, #FFD700 0%, #FDB931 100%);
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
        border-radius: 50%;
    }

    /* ========== INPUT BOX STYLING ========== */
    .stChatInputContainer {
        padding: 16px 0 !important;
        background: transparent !important;
        border-top: 1px solid rgba(255, 215, 0, 0.1);
    }
    
    .stChatInputContainer textarea {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.8) 0%, rgba(30, 25, 50, 0.8) 100%) !important;
        color: #e8eaed !important;
        border: 1.5px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 15px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: none !important;
    }

    .stChatInputContainer textarea:focus {
        background: linear-gradient(135deg, rgba(25, 25, 50, 0.95) 0%, rgba(35, 30, 60, 0.95) 100%) !important;
        border-color: rgba(255, 215, 0, 0.5) !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.15) !important;
        outline: none !important;
    }

    .stChatInputContainer textarea::placeholder {
        color: rgba(232, 234, 237, 0.5) !important;
        font-style: italic;
    }

    /* ========== HEADER STYLING ========== */
    .main-header {
        text-align: center;
        padding: 50px 30px 40px;
        border-bottom: 2px solid rgba(255, 215, 0, 0.2);
        margin-bottom: 35px;
        position: relative;
        overflow: hidden;
        animation: headerIn 0.8s ease-out;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 0%, rgba(255, 215, 0, 0.05), transparent);
        pointer-events: none;
    }

    @keyframes headerIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header h1 {
        background: linear-gradient(135deg, #FFD700 0%, #FDB931 50%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: -1px;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
        margin-bottom: 12px;
    }

    .main-header p {
        color: #a0a9c9;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 600;
        word-spacing: 8px;
    }

    /* ========== CITATION/EVIDENCE CARD ========== */
    .citation-card {
        background: linear-gradient(135deg, rgba(25, 25, 45, 0.8) 0%, rgba(35, 30, 60, 0.6) 100%);
        border-left: 5px solid #FFD700;
        border-right: 1px solid rgba(255, 215, 0, 0.2);
        border-top: 1px solid rgba(255, 215, 0, 0.15);
        border-bottom: 1px solid rgba(255, 215, 0, 0.15);
        padding: 18px 20px;
        margin: 12px 0;
        border-radius: 8px;
        font-size: 0.95em;
        color: #d4d6da;
        line-height: 1.6;
        backdrop-filter: blur(15px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .citation-card:hover {
        background: linear-gradient(135deg, rgba(35, 35, 60, 0.9) 0%, rgba(45, 40, 75, 0.7) 100%);
        border-left-color: #FFE044;
        border-right-color: rgba(255, 215, 0, 0.3);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.1);
        transform: translateX(4px);
    }

    .citation-header {
        font-weight: 700;
        color: #FFD700;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-size: 0.75em;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ========== EXPANDER STYLING ========== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, rgba(255, 215, 0, 0.05) 100%) !important;
        border: 1px solid rgba(255, 215, 0, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        color: #FFD700 !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 215, 0, 0.08) 100%) !important;
        border-color: rgba(255, 215, 0, 0.4) !important;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.1) !important;
    }

    /* ========== SIDEBAR STYLING ========== */
    .sidebar-content {
        background: linear-gradient(135deg, rgba(20, 20, 40, 0.8) 0%, rgba(30, 25, 50, 0.8) 100%);
        border-right: 1px solid rgba(255, 215, 0, 0.15);
        padding: 25px;
        border-radius: 0 16px 16px 0;
    }

    /* ========== STATUS BADGE ========== */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 4px 0;
    }

    .status-online {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.1) 100%);
        color: #4cb050;
        border: 1px solid rgba(76, 175, 80, 0.3);
    }

    .status-secure {
        background: linear-gradient(135deg, rgba(25, 118, 210, 0.2) 0%, rgba(25, 118, 210, 0.1) 100%);
        color: #1976d2;
        border: 1px solid rgba(25, 118, 210, 0.3);
    }

    /* ========== MARKDOWN TEXT ========== */
    .stMarkdown h2 {
        color: #FFD700 !important;
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    .stMarkdown h3 {
        color: #e8eaed !important;
        font-weight: 600 !important;
    }

    .stMarkdown code {
        background: rgba(255, 215, 0, 0.1) !important;
        color: #FFD700 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 500;
    }

    /* ========== ERROR MESSAGE ========== */
    .stError {
        background: linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(244, 67, 54, 0.1) 100%) !important;
        border: 1px solid rgba(244, 67, 54, 0.3) !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        color: #ffb3b3 !important;
    }

    /* ========== INFO MESSAGE ========== */
    .stInfo {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(33, 150, 243, 0.1) 100%) !important;
        border: 1px solid rgba(33, 150, 243, 0.3) !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
        color: #b3d9ff !important;
    }

    /* ========== LOADING STATE ========== */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    .loading-state {
        animation: pulse 2s ease-in-out infinite;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 215, 0, 0.05);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FDB931);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFE044, #FFDB58);
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header {
            padding: 30px 15px 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PREMIUM UI LAYOUT ---

# Header with enhanced animation
st.markdown("""
<div class="main-header">
    <h1>⚖️ NYAYA SAHAYAK</h1>
    <p style="color: #a0a9c9; letter-spacing: 3px; text-transform: uppercase; font-size: 0.8rem; font-weight: 600; word-spacing: 6px;">
        Advanced AI Legal Intelligence System • BNS 2023
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar with modern design
with st.sidebar:
    st.markdown("### 💼 Control Center")
    st.info("💡 **Tip:** Ask about punishments, sections, or definitions. The AI retrieves real legal text.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="status-badge status-online">🟢 ONLINE</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="status-badge status-secure">🔒 SECURE</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**About:**")
    st.caption("Powered by LangChain + Gemini API")
    st.caption("Vector Database: Chroma")

# --- 4. CHAT LOGIC WITH ENHANCED VISUALS ---

# Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display OLD messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="⚖️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])
        
        # Display sources with enhanced styling
        if "sources" in message:
            with st.expander("📂 View Legal Evidence", expanded=False):
                for idx, source in enumerate(message["sources"], 1):
                    st.markdown(f"""
                    <div class="citation-card">
                        <div class="citation-header">📋 EXHIBIT {idx}</div>
                        {source}
                    </div>
                    """, unsafe_allow_html=True)

# Handle NEW Input
if prompt := st.chat_input("Enter your legal query here..."):
    # 1. Show User Message Immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate Response with animated loading
    with st.chat_message("assistant", avatar="⚖️"):
        message_placeholder = st.empty()
        
        # Animated loading state
        message_placeholder.markdown(
            '<div class="loading-state">⚡ <b>Analyzing BNS 2023 Database...</b></div>',
            unsafe_allow_html=True
        )
        
        try:
            # Call RAG Logic
            response_data = get_answer(prompt)
            full_response = response_data['result']
            source_docs = response_data['source_documents']
            
            # Clean up sources for display
            clean_sources = [doc.page_content[:400] + "..." for doc in source_docs]
            
            # Show Final Answer
            message_placeholder.markdown(full_response)
            
            # Show Evidence Cards with enhanced styling
            if clean_sources:
                st.markdown("---")
                with st.expander("📂 Click to Verify Legal Evidence", expanded=False):
                    for idx, src in enumerate(clean_sources, 1):
                        st.markdown(f"""
                        <div class="citation-card">
                            <div class="citation-header">📋 EXHIBIT {idx}</div>
                            {src}
                        </div>
                        """, unsafe_allow_html=True)

            # Save to History
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "sources": clean_sources
            })
            
        except Exception as e:
            message_placeholder.error(f"⚠️ System Error: {str(e)}")

