"""
Main Entry Point - Multi-Domain Intelligence Platform
"""

import streamlit as st

# Set page config - MUST BE FIRST
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

def main():
    """Main application logic."""
    
    # Header
    st.title("🏢 Multi-Domain Intelligence Platform")
    
    # Check login status
    if st.session_state.logged_in:
        show_dashboard_redirect()
    else:
        show_login_redirect()
    
    # Sidebar info
    with st.sidebar:
        st.markdown("## 🔍 Navigation")
        
        if st.session_state.logged_in:
            st.success(f"Welcome, {st.session_state.username}!")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.rerun()
        else:
            st.info("Please log in to access the platform")
        
        st.markdown("---")
        st.markdown("### Demo Credentials")
        st.code("Username: john_analyst\nPassword: password123")

def show_dashboard_redirect():
    """Redirect to dashboard or show dashboard directly."""
    st.success("✅ You are logged in!")
    
    # Try to redirect to dashboard page
    try:
        # Use JavaScript redirect for better compatibility
        js = '''
        <script>
            window.location.href = "/Dashboard";
        </script>
        '''
        st.components.v1.html(js, height=0)
    except:
        # Fallback: show dashboard directly
        st.info("Loading dashboard...")
        try:
            from pages.dashboard import main as dashboard_main
            dashboard_main()
        except Exception as e:
            st.error(f"Could not load dashboard: {str(e)}")
            st.info("Using simplified dashboard view...")
            show_simple_dashboard()

def show_login_redirect():
    """Redirect to login page."""
    st.info("🔐 Please log in to continue")
    
    # Try to redirect to login page
    try:
        # Use JavaScript redirect for better compatibility
        js = '''
        <script>
            window.location.href = "/Login";
        </script>
        '''
        st.components.v1.html(js, height=0)
    except:
        # Fallback: show simple login form
        show_simple_login()

def show_simple_login():
    """Fallback simple login form."""
    st.subheader("Login")
    
    with st.form("login_form"):
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
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials. Try: john_analyst / password123")

def show_simple_dashboard():
    """Fallback simple dashboard."""
    st.subheader("Dashboard")
    
    # Create tabs for different domains
    tab1, tab2, tab3 = st.tabs(["🔒 Cybersecurity", "📊 Data Science", "🖥️ IT Operations"])
    
    with tab1:
        st.write("Cybersecurity dashboard would appear here")
        st.info("Sample security metrics")
        
    with tab2:
        st.write("Data Science dashboard would appear here")
        st.info("Sample data analytics")
        
    with tab3:
        st.write("IT Operations dashboard would appear here")
        st.info("Sample IT metrics")

if __name__ == "__main__":
    main()