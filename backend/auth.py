"""
Authentication and Session Management
Handles login/signup flows and user session state
"""

import streamlit as st
from backend.database import db
import json

class AuthManager:
    """Manages user authentication and session state"""
    
    @staticmethod
    def init_session():
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'user_name' not in st.session_state:
            st.session_state.user_name = None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is currently authenticated"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def login(email: str, password: str) -> tuple[bool, str]:
        """
        Attempt to login user
        Returns: (success: bool, message: str)
        """
        result = db.login_user(email, password)
        
        if result['success']:
            st.session_state.authenticated = True
            st.session_state.user_email = result['email']
            st.session_state.user_id = result['user_id']
            
            # Fetch user details
            user = db.get_user(email)
            if user:
                st.session_state.user_name = user['full_name']
            
            return True, result['message']
        
        return False, result['message']
    
    @staticmethod
    def signup(email: str, full_name: str, password: str, password_confirm: str) -> tuple[bool, str]:
        """
        Attempt to register new user
        Returns: (success: bool, message: str)
        """
        # Validate password confirmation
        if password != password_confirm:
            return False, "Passwords do not match"
        
        result = db.register_user(email, full_name, password)
        return result['success'], result['message']
    
    @staticmethod
    def logout():
        """Logout current user and clear session"""
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.session_state.user_name = None
    
    @staticmethod
    def get_current_user() -> dict:
        """Get current authenticated user details"""
        if not AuthManager.is_authenticated():
            return None
        
        return {
            'id': st.session_state.user_id,
            'email': st.session_state.user_email,
            'name': st.session_state.user_name
        }
    
    @staticmethod
    def require_login(func):
        """Decorator to protect pages that require authentication"""
        def wrapper(*args, **kwargs):
            if not AuthManager.is_authenticated():
                st.error("Please login or signup to access this page")
                return
            return func(*args, **kwargs)
        return wrapper


def render_login_page():
    """Render the login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1>⚖️ NyayaSahayak</h1>
            <p style='font-size: 18px; color: #888;'>Your Legal AI Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Welcome Back")
        
        email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            key="login_email"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        col_login, col_signup = st.columns(2)
        
        with col_login:
            if st.button("🔓 Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    success, message = AuthManager.login(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col_signup:
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()


def render_signup_page():
    """Render the signup page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <h1>⚖️ NyayaSahayak</h1>
            <p style='font-size: 18px; color: #888;'>Your Legal AI Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Create New Account")
        
        full_name = st.text_input(
            "Full Name",
            placeholder="John Doe",
            key="signup_name"
        )
        
        email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            key="signup_email"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="signup_password",
            help="Must contain: uppercase, lowercase, number, and special character (!@#$%^&*)"
        )
        
        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm"
        )
        
        # Password strength indicator
        if password:
            strength = _check_password_strength(password)
            st.markdown(f"**Password Strength:** {strength['text']}")
            st.progress(strength['score'] / 100)
        
        st.markdown("""
        <small style='color: #888;'>
        Password Requirements:
        • At least 8 characters
        • Uppercase and lowercase letters
        • At least one number
        • At least one special character (!@#$%^&*)
        </small>
        """, unsafe_allow_html=True)
        
        col_create, col_back = st.columns(2)
        
        with col_create:
            if st.button("✅ Create Account", use_container_width=True, type="primary"):
                if not full_name or not email or not password:
                    st.error("Please fill in all fields")
                else:
                    success, message = AuthManager.signup(email, full_name, password, password_confirm)
                    if success:
                        st.success(message)
                        st.info("Account created! Please login now.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error(message)
        
        with col_back:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()


def _check_password_strength(password: str) -> dict:
    """Check password strength and return score"""
    score = 0
    
    if len(password) >= 8:
        score += 20
    if any(c.isupper() for c in password):
        score += 20
    if any(c.islower() for c in password):
        score += 20
    if any(c.isdigit() for c in password):
        score += 20
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        score += 20
    
    if score >= 100:
        return {"score": 100, "text": "🟢 Strong"}
    elif score >= 60:
        return {"score": score, "text": "🟡 Medium"}
    else:
        return {"score": score, "text": "🔴 Weak"}


def render_auth_page():
    """Main authentication page that handles login/signup flow"""
    AuthManager.init_session()
    
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    if st.session_state.show_signup:
        render_signup_page()
    else:
        render_login_page()
