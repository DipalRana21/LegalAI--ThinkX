"""
Streamlit Frontend Application
Main entry point for the Legal Assistance System
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Disable TensorFlow to avoid compatibility issues with transformers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['DISABLE_TF'] = '1'

# Patch importlib.util.find_spec to prevent TensorFlow detection
import sys
import importlib.util

# Save original find_spec
_original_find_spec = importlib.util.find_spec

def patched_find_spec(name, package=None):
    """Patched find_spec that returns None for tensorflow"""
    if name == 'tensorflow' or (isinstance(name, str) and name.startswith('tensorflow')):
        return None  # Pretend tensorflow doesn't exist
    return _original_find_spec(name, package)

# Monkey patch find_spec
importlib.util.find_spec = patched_find_spec

# Add parent directory to path for backend imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Lazy imports - only import backend modules when needed to speed up startup
# Import config module to avoid triggering heavy module imports
import backend.config as config

# Page configuration
st.set_page_config(
    page_title="Legal Assistance System - Indian Laws",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f4788;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2a5aa0;
    }
    .answer-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f4788;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
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


def initialize_system():
    """Initialize the RAG system"""
    try:
        # Lazy import heavy modules only when needed
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
            # Try importing the module first, then the class
            import backend.rag_chain as rag_chain_module
            if not hasattr(rag_chain_module, 'RAGChain'):
                st.error("RAGChain class not found in backend.rag_chain module")
                st.error(f"Available attributes: {[x for x in dir(rag_chain_module) if not x.startswith('_')]}")
                return False
            RAGChain = rag_chain_module.RAGChain
        except ImportError as e:
            st.error(f"Failed to import RAGChain module: {str(e)}")
            import traceback
            st.error(f"Traceback:\n```\n{traceback.format_exc()}\n```")
            return False
        except Exception as e:
            st.error(f"Failed to import RAGChain: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            import traceback
            st.error(f"Traceback:\n```\n{traceback.format_exc()}\n```")
            return False
        
        with st.spinner("Initializing Legal Assistance System..."):
            # Check if vector store exists
            if os.path.exists(config.VECTOR_STORE_PATH) and os.listdir(config.VECTOR_STORE_PATH):
                # Load existing vector store
                vector_store_manager = VectorStoreManager(config.VECTOR_STORE_PATH)
                vector_store_manager.load_vector_store()
            else:
                # Create new vector store
                st.info("First-time setup: Processing PDF documents...")
                
                # Process PDFs
                pdf_processor = PDFProcessor(
                    chunk_size=config.CHUNK_SIZE,
                    chunk_overlap=config.CHUNK_OVERLAP
                )
                
                # Get all PDF files
                pdf_files = []
                for pdf_file in config.PDF_FILES:
                    if os.path.exists(pdf_file):
                        pdf_files.append(pdf_file)
                
                if not pdf_files:
                    st.error("No PDF files found! Please ensure PDF files are in the project directory.")
                    return False
                
                # Process documents
                documents = pdf_processor.process_multiple_pdfs(pdf_files)
                
                if not documents:
                    st.error("No documents could be processed from PDF files.")
                    return False
                
                # Create vector store
                vector_store_manager = VectorStoreManager(config.VECTOR_STORE_PATH)
                vector_store_manager.create_vector_store(documents)
                vector_store_manager.save_vector_store()
            
            # Initialize RAG chain
            if not config.GOOGLE_API_KEY:
                st.error("⚠️ Google API Key not found! Please set GOOGLE_API_KEY in .env file")
                return False
            
            rag_chain = RAGChain(vector_store_manager)
            st.session_state.rag_chain = rag_chain
            st.session_state.vector_store_initialized = True
            
            return True
            
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")
        return False


def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ Legal Assistance System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Legal Information Assistant for Indian Laws</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Clear chat history
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    if not st.session_state.vector_store_initialized:
        st.info("👈 Please initialize the system from the sidebar to begin.")
        
        # Auto-initialize if API key is available
        if config.GOOGLE_API_KEY:
            if initialize_system():
                st.rerun()
    else:
        # Chat interface
        st.header("💬 Ask Your Legal Question")
        
        # Display chat history
        for i, (question, answer, sources) in enumerate(st.session_state.chat_history):
            with st.expander(f"Q: {question}", expanded=(i == len(st.session_state.chat_history) - 1)):
                st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)
        
        # Query input
        query = st.text_area(
            "Enter your legal question:",
            height=100,
            placeholder="Example: What are the penalties for cybercrime under Indian law?"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit_button = st.button("🔍 Search", use_container_width=True, type="primary")
        
        # Process query
        if submit_button and query:
            if st.session_state.rag_chain:
                with st.spinner("🔍 Searching legal documents and generating answer..."):
                    result = st.session_state.rag_chain.query(query)
                    
                    answer = result["answer"]
                    sources = result.get("source_documents", [])
                    
                    # Add to chat history
                    st.session_state.chat_history.append((query, answer, sources))
                    
                    # Rerun to show new answer
                    st.rerun()
            else:
                st.error("RAG chain not initialized. Please reinitialize the system.")


if __name__ == "__main__":
    main()

