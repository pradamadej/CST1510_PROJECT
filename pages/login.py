"""
Login Page - Updated for OpenAI 0.28.1
"""

import streamlit as st
import sys
import os
import bcrypt

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database_manager import DatabaseManager
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    # Fallback DatabaseManager
    class DatabaseManager:
        def get_user_by_username(self, username):
            demo_users = {
                'john_analyst': (1, 'john_analyst', 
                               '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
                               'cyber_analyst', '2024-01-01'),
                'sara_scientist': (2, 'sara_scientist',
                                  '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
                                  'data_scientist', '2024-01-01'),
                'mike_admin': (3, 'mike_admin',
                              '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
                              'it_administrator', '2024-01-01')
            }
            return demo_users.get(username)

# Page config
st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# Initialize session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def verify_password(plain, hashed):
    """Verify password."""
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except:
        return plain == "password123"  # Fallback for demo

def login_user(username, password):
    """Authenticate user."""
    try:
        db = DatabaseManager()
        user = db.get_user_by_username(username)
        
        if user:
            user_id, stored_user, stored_hash, role, created = user
            
            if verify_password(password, stored_hash):
                return True, {
                    'user_id': user_id,
                    'username': stored_user,
                    'role': role
                }
            else:
                return False, "Invalid password"
        else:
            return False, "User not found"
    except Exception as e:
        return False, str(e)

def main():
    """Main login function."""
    
    # If already logged in, redirect
    if st.session_state.get('logged_in'):
        st.success(f"Welcome back, {st.session_state.username}!")
        if st.button("Go to Dashboard"):
            st.switch_page("pages/2_Dashboard.py")
        return
    
    # Login form
    st.title("🔐 Login")
    
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                success, result = login_user(username, password)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = result['username']
                    st.session_state.user_role = result['role']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {result}")
            else:
                st.error("Please enter both username and password")
    
    # Demo info
    with st.expander("Demo Accounts"):
        st.write("""
        **Available accounts:**
        - john_analyst / password123
        - sara_scientist / password123  
        - mike_admin / password123
        """)

if __name__ == "__main__":
    main()