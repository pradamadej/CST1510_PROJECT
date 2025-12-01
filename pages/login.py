"""
Login Page for Multi-Domain Intelligence Platform
File: pages/1_Login.py
"""

import streamlit as st
import sys
import os
import bcrypt

# Add project root to path for imports
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, proj_root)

# Import DatabaseManager from the correct module
try:
    from database_manager import DatabaseManager
    DB_MANAGER_AVAILABLE = True
except ImportError:
    DB_MANAGER_AVAILABLE = False
    st.error("DatabaseManager not found. Please ensure database_manager.py is in the project root.")
    
    # Create a fallback DatabaseManager for demonstration
    class DatabaseManager:
        def __init__(self, db_name="intelligence_platform.db"):
            self.db_name = db_name
            self.demo_users = {
                'john_analyst': {
                    'id': 1,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'cyber_analyst',
                    'created_at': '2024-01-01 00:00:00'
                },
                'sara_scientist': {
                    'id': 2,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'data_scientist',
                    'created_at': '2024-01-01 00:00:00'
                },
                'mike_admin': {
                    'id': 3,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'it_administrator',
                    'created_at': '2024-01-01 00:00:00'
                },
                'Joel_analyst': {
                    'id': 4,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'cyber_analyst',
                    'created_at': '2024-01-01 00:00:00'
                },
                'Sara_scientist': {
                    'id': 5,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'data_scientist',
                    'created_at': '2024-01-01 00:00:00'
                },
                'Daniel_admin': {
                    'id': 6,
                    'password_hash': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 'password123' hashed
                    'role': 'it_administrator',
                    'created_at': '2024-01-01 00:00:00'
                }
            }
        
        def get_user_by_username(self, username):
            """Fallback method to get user by username."""
            user_data = self.demo_users.get(username)
            if user_data:
                return (
                    user_data['id'],
                    username,
                    user_data['password_hash'],
                    user_data['role'],
                    user_data['created_at']
                )
            return None
        
        def execute_query(self, query, params=()):
            """Fallback execute_query method."""
            return []
        
        def close(self):
            """Fallback close method."""
            pass

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
        # For demo purposes, if bcrypt fails, check if it's the demo password
        if plain_password == "password123":
            return True
        return False

def login_user(username, password):
    """
    Authenticate user credentials.
    
    Args:
        username (str): The username
        password (str): The password
        
    Returns:
        tuple: (success, user_data) where success is boolean and user_data is dict or error message
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
        return False, f"Login error: {str(e)}"

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
        | `Joel_analyst` | `password123` | Cyber Analyst | Cybersecurity Dashboard |
        | `Sara_scientist` | `password123` | Data Scientist | Data Science Dashboard |
        | `Daniel_admin` | `password123` | IT Administrator | IT Operations Dashboard |
        
        ### Role-Based Access:
        - **Cyber Analyst**: Access to security incidents, threat analysis
        - **Data Scientist**: Access to datasets, data quality metrics  
        - **IT Administrator**: Access to IT tickets, system performance
        
        *Note: All demo accounts use password: `password123`*
        """)

def show_registration_info():
    """Display information about user registration."""
    with st.expander("📝 Need an Account?"):
        st.info("""
        **User Registration:**
        
        Currently using demo accounts. To add new users:
        
        1. **Database Migration**: Use the `migrate_users_from_file()` method in DatabaseManager
        2. **Manual Setup**: Add users directly to the database
        3. **Command Line**: Run the user migration script
        
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
        st.info("You are already logged in.")
        
        # Add buttons to go to dashboard or logout
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/2_Dashboard.py")
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                for key in ['logged_in', 'username', 'user_role', 'user_id']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        return
    
    # Show login form
    username, password, login_button, clear_button = show_login_form()
    
    # Show informational sections
    show_user_roles_info()
    show_registration_info()
    
    # Database availability warning
    if not DB_MANAGER_AVAILABLE:
        st.warning("⚠️ Using fallback DatabaseManager with demo accounts only")
    
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
                        st.info("💡 Try one of the demo accounts listed above")
                    elif "Invalid password" in error_message:
                        st.info("💡 For demo accounts, use password: `password123`")

def create_demo_users():
    """
    Utility function to create demo users if they don't exist.
    This would typically be run once during setup.
    """
    try:
        db = DatabaseManager()
        
        demo_users = [
            {
                'username': 'john_analyst',
                'password': 'password123',
                'role': 'cyber_analyst'
            },
            {
                'username': 'sara_scientist', 
                'password': 'password123',
                'role': 'data_scientist'
            },
            {
                'username': 'mike_admin',
                'password': 'password123', 
                'role': 'it_administrator'
            },
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
            # Check if user exists - using get_user_by_username
            existing = db.get_user_by_username(user_data['username'])
            if not existing:
                try:
                    # Hash password
                    hashed_pw = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    # Create user - using insert_record if available
                    if hasattr(db, 'insert_record'):
                        db.insert_record('users', {
                            'username': user_data['username'],
                            'password_hash': hashed_pw,
                            'role': user_data['role']
                        })
                        created_count += 1
                    else:
                        print(f"insert_record method not available in DatabaseManager")
                except Exception as e:
                    print(f"Error creating user {user_data['username']}: {e}")
        
        db.close()
        if created_count > 0:
            print(f"Created {created_count} demo users")
            
    except Exception as e:
        print(f"Error creating demo users: {e}")

if __name__ == "__main__":
    main()