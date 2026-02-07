"""
NyayaSahayak - Authenticated Main Entry Point
Handles login/signup gating before accessing the main legal assistant
"""

import streamlit as st
import sys
from pathlib import Path
import os

# Setup path
parent_dir = Path(__file__).parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(parent_dir.parent))

from backend.auth import AuthManager, render_auth_page

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="NyayaSahayak - Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== GLOBAL STYLING ==============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

* {
    margin: 0;
    padding: 0;
}

.main {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1535 50%, #0d0c1d 100%);
    color: #e8eaed;
}

html, body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1535 50%, #0d0c1d 100%);
}

/* Auth page styling */
.auth-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
}

.stButton > button {
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #ddd;
    padding: 10px 15px;
    font-size: 16px;
}

.stTextInput > div > div > input:focus {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.1);
}

.auth-card {
    background: rgba(30, 30, 46, 0.6);
    border: 1px solid rgba(255, 215, 0, 0.15);
    border-radius: 16px;
    padding: 30px;
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.user-info {
    background: rgba(245, 158, 11, 0.1);
    border-left: 4px solid #f59e0b;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Initialize authentication
AuthManager.init_session()

# If not authenticated, show login/signup page
if not AuthManager.is_authenticated():
    render_auth_page()
else:
    # User is authenticated - show the main app
    user = AuthManager.get_current_user()
    
    # Sidebar for authenticated user
    with st.sidebar:
        st.markdown("""
        <div style='padding: 10px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 20px;'>
            <p style='margin: 0; color: #888; font-size: 12px; text-transform: uppercase;'>Logged in as</p>
            <p style='margin: 5px 0 0 0; font-weight: 600; font-size: 16px;'>{}</p>
            <p style='margin: 2px 0 0 0; font-size: 12px; color: #666;'>{}</p>
        </div>
        """.format(user['name'], user['email']), unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            AuthManager.logout()
            st.success("You have been logged out successfully")
            st.rerun()
        
        st.divider()
    
    # Import and run the main legal AI app
    # Disable TensorFlow to avoid compatibility issues
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
    
    try:
        # Import the app module from the same directory
        spec = importlib.util.spec_from_file_location("legal_app", str(Path(__file__).parent / "app.py"))
        legal_app = importlib.util.module_from_spec(spec)
        sys.modules["legal_app"] = legal_app
        spec.loader.exec_module(legal_app)
        
        # Call the main function
        legal_app.main()
    except Exception as e:
        st.error(f"Error loading main application: {str(e)}")
        st.warning(f"Details: {str(e)}")
        st.info("Make sure app.py has a main() function defined.")

