"""
Main Application Entry Point for Multi-Domain Intelligence Platform
File: app.py
"""

import streamlit as st
import sys
import os

# Set page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to path for imports
proj_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, proj_root)

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def main():
    """Main application entry point."""
    
    # Sidebar navigation
    st.sidebar.title("🏢 Navigation")
    
    # Check if user is logged in
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as: {st.session_state.username}")
        st.sidebar.info(f"Role: {st.session_state.user_role}")
        
        # Navigation options for logged in users
        page_option = st.sidebar.radio(
            "Go to:",
            ["Dashboard", "Logout"]
        )
        
        if page_option == "Dashboard":
            # Import and run dashboard
            try:
                from pages.dashboard import main as dashboard_main
                dashboard_main()
            except ImportError:
                st.error("Dashboard page not found")
                st.info("Make sure pages/dashboard.py exists")
        elif page_option == "Logout":
            if st.sidebar.button("Confirm Logout", type="primary"):
                # Clear session state
                for key in ['logged_in', 'username', 'user_role', 'user_id']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    
    else:
        # User is not logged in - show login options
        st.sidebar.warning("You are not logged in")
        
        page_option = st.sidebar.radio(
            "Go to:",
            ["Login", "About"]
        )
        
        if page_option == "Login":
            # Import and run login page
            try:
                from pages.login import main as login_main
                login_main()
            except ImportError:
                # Fallback to simple login form
                show_simple_login()
        elif page_option == "About":
            show_about_page()

def show_simple_login():
    """Fallback simple login form if login page can't be imported."""
    st.title("🔐 Multi-Domain Intelligence Platform")
    st.markdown("### Simple Login")
    
    with st.form("simple_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            # Simple demo authentication
            demo_users = {
                'john_analyst': 'password123',
                'sara_scientist': 'password123',
                'mike_admin': 'password123',
                'Joel_analyst': 'password123',
                'Sara_scientist': 'password123',
                'Daniel_admin': 'password123'
            }
            
            if username in demo_users and password == demo_users[username]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = "demo_user"
                st.session_state.user_id = 1
                st.success("Login successful! Please refresh to access dashboard.")
                st.rerun()
            else:
                st.error("Invalid credentials. Try 'john_analyst' with 'password123'")

def show_about_page():
    """Show about information."""
    st.title("🏢 About Multi-Domain Intelligence Platform")
    
    st.markdown("""
    ## Platform Overview
    
    This multi-domain intelligence platform integrates three key domains:
    
    ### 🔒 Cybersecurity
    - Monitor security incidents
    - Track threat levels
    - Manage incident response
    
    ### 📊 Data Science  
    - Analyze dataset quality
    - Monitor data governance
    - Track data usage metrics
    
    ### 🖥️ IT Operations
    - Manage IT support tickets
    - Track system performance
    - Monitor resolution times
    
    ## Features
    
    - **Role-based access control**
    - **AI-powered analytics**
    - **Real-time dashboards**
    - **Interactive visualizations**
    - **Secure authentication**
    
    ## Getting Started
    
    1. Use the sidebar to navigate to Login
    2. Use demo credentials:
       - Username: `john_analyst`
       - Password: `password123`
    3. Access domain-specific dashboards based on your role
    """)
    
    # Demo credentials table
    st.markdown("### Demo Credentials")
    demo_data = {
        "Username": ["john_analyst", "sara_scientist", "mike_admin", 
                    "Joel_analyst", "Sara_scientist", "Daniel_admin"],
        "Password": ["password123", "password123", "password123",
                    "password123", "password123", "password123"],
        "Role": ["Cyber Analyst", "Data Scientist", "IT Administrator",
                "Cyber Analyst", "Data Scientist", "IT Administrator"]
    }
    st.table(demo_data)

# Clean up function to avoid circular imports
def safe_import_page(page_name):
    """Safely import a page module."""
    try:
        if page_name == "login":
            from pages.login import main as page_main
            return page_main
        elif page_name == "dashboard":
            from pages.dashboard import main as page_main
            return page_main
    except ImportError as e:
        st.error(f"Error importing {page_name}: {e}")
        return None

if __name__ == "__main__":
    main()