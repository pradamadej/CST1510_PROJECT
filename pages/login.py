"""
Login Page for Multi-Domain Intelligence Platform
File: pages/1_Login.py
"""

import streamlit as st
import sys
import os

# Ensure the Database.db folder is on sys.path so we can import the local database module
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_folder = os.path.join(proj_root, "Database.db")
if db_folder not in sys.path:
    sys.path.insert(0, db_folder)

# Import DatabaseManager from the local `database.py` module inside Database.db
from database import DatabaseManager
import bcrypt

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        plain_password (str): The password to verify
        hashed_password (str): The stored hash to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        st.error(f"Password verification error: {e}")
        return False

def login_user(username, password):
    """
    Authenticate user credentials.
    
    Args:
        username (str): The username
        password (str): The password
        
    Returns:
        tuple: (success, user_data) where success is boolean and user_data is dict
    """
    try:
        db = DatabaseManager()
        
        # Get user from database
        user = db.get_user_by_username(username)
        db.close()
        
        if user:
            user_id, stored_username, stored_hash, role, created_at = user
            
            # Verify password
            if verify_password(password, stored_hash):
                return True, {
                    'user_id': user_id,
                    'username': stored_username,
                    'role': role,
                    'created_at': created_at
                }
            else:
                return False, "Invalid password"
        else:
            return False, "User not found"
            
    except Exception as e:
        return False, f"Login error: {e}"

def show_login_form():
    """Display the login form."""
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.title("🔐 Multi-Domain Intelligence Platform")
    st.markdown("### Sign In to Your Account")
    st.markdown("---")
    
    # Login form
    with st.form("login_form"):
        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username",
            help="Your registered username"
        )
        
        password = st.text_input(
            "🔒 Password", 
            type="password",
            placeholder="Enter your password",
            help="Your account password"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🔄 Clear", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return username, password, login_button, clear_button

def show_user_roles_info():
    """Display information about different user roles and demo accounts."""
    with st.expander("💡 Demo Accounts & Role Information"):
        st.markdown("""
        ### Available Demo Accounts:
        
        | Username | Password | Role | Access |
        |----------|----------|------|--------|
        | `john_analyst` | `password123` | Cyber Analyst | Cybersecurity Dashboard |
        | `sara_scientist` | `password123` | Data Scientist | Data Science Dashboard |
        | `mike_admin` | `password123` | IT Administrator | IT Operations Dashboard |
        
        ### Role-Based Access:
        - **Cyber Analyst**: Access to security incidents, threat analysis
        - **Data Scientist**: Access to datasets, data quality metrics  
        - **IT Administrator**: Access to IT tickets, system performance
        
        *Note: These are demo accounts with hashed passwords for testing.*
        """)

def show_registration_info():
    """Display information about user registration."""
    with st.expander("📝 Need an Account?"):
        st.info("""
        **User Registration:**
        
        To create a new account, you'll need to:
        1. Use the command-line registration system from Week 7
        2. Or ask your administrator to create an account for you
        3. Demo accounts are available for testing (see above)
        
        *Web-based registration will be available in future updates.*
        """)

def main():
    """Main login page function."""
    # Set page configuration
    st.set_page_config(
        page_title="Login - Intelligence Platform",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Hide Streamlit menu and footer for clean login page
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # If user is already logged in, redirect to dashboard
    if st.session_state.logged_in:
        st.success(f"Welcome back, {st.session_state.username}!")
        st.info("Redirecting to dashboard...")
        
        # Add a button to go to dashboard
        if st.button("🚀 Go to Dashboard"):
            st.switch_page("pages/2_Dashboard.py")
        return
    
    # Show login form
    username, password, login_button, clear_button = show_login_form()
    
    # Show informational sections
    show_user_roles_info()
    show_registration_info()
    
    # Handle form actions
    if clear_button:
        st.rerun()
    
    if login_button:
        if not username or not password:
            st.error("❌ Please enter both username and password")
        else:
            # Show loading spinner
            with st.spinner("Authenticating..."):
                success, result = login_user(username, password)
                
                if success:
                    user_data = result
                    
                    # Update session state
                    st.session_state.logged_in = True
                    st.session_state.username = user_data['username']
                    st.session_state.user_role = user_data['role']
                    st.session_state.user_id = user_data['user_id']
                    
                    st.success(f"✅ Login successful! Welcome, {user_data['username']}!")
                    st.balloons()
                    
                    # Redirect to dashboard after a short delay
                    st.info("Redirecting to dashboard...")
                    st.switch_page("pages/2_Dashboard.py")
                    
                else:
                    error_message = result
                    st.error(f"❌ Login failed: {error_message}")
                    
                    # Show helpful suggestions based on error
                    if "User not found" in error_message:
                        st.info("💡 Check the demo accounts above or contact your administrator")
                    elif "Invalid password" in error_message:
                        st.info("💡 Please check your password and try again")

def create_demo_users():
    """
    Utility function to create demo users if they don't exist.
    This would typically be run once during setup.
    """
    try:
        db = DatabaseManager()
        
        demo_users = [
            {
                'username': 'Joel_analyst',
                'password': 'password123',
                'role': 'cyber_analyst'
            },
            {
                'username': 'Sara_scientist', 
                'password': 'password123',
                'role': 'data_scientist'
            },
            {
                'username': 'Daniel_admin',
                'password': 'password123', 
                'role': 'it_administrator'
            }
        ]
        
        created_count = 0
        for user_data in demo_users:
            # Check if user exists
            existing = db.get_user_by_username(user_data['username'])
            if not existing:
                # Hash password
                hashed_pw = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Create user
                db.create_user({
                    'username': user_data['username'],
                    'password_hash': hashed_pw,
                    'role': user_data['role']
                })
                created_count += 1
        
        db.close()
        if created_count > 0:
            print(f"Created {created_count} demo users")
            
    except Exception as e:
        print(f"Error creating demo users: {e}")

if __name__ == "__main__":
    main()