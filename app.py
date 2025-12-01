"""
Main Entry Point - Multi-Domain Intelligence Platform
"""

import streamlit as st
import os

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
if 'openai_available' not in st.session_state:
    st.session_state.openai_available = False
if 'openai_error' not in st.session_state:
    st.session_state.openai_error = None

def initialize_openai():
    """Initialize OpenAI client with API key from secrets."""
    try:
        # Get API key from Streamlit secrets or environment
        api_key = None
        
        # Try Streamlit secrets first
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
        except:
            pass
        
        # Try environment variable
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == "":
            st.session_state.openai_available = False
            st.session_state.openai_error = "API key not found"
            return None
        
        # Import OpenAI here to avoid issues
        from openai import OpenAI
        
        # Simple initialization without extra parameters
        client = OpenAI(api_key=api_key)
        
        # Test the connection with a simple call
        try:
            # Quick test to verify API works
            test_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'ok'"}],
                max_tokens=5
            )
            st.session_state.openai_available = True
            st.session_state.openai_error = None
            return client
        except Exception as test_error:
            st.session_state.openai_available = False
            st.session_state.openai_error = f"API test failed: {str(test_error)}"
            return None
            
    except ImportError:
        st.session_state.openai_available = False
        st.session_state.openai_error = "OpenAI package not installed"
        return None
    except Exception as e:
        st.session_state.openai_available = False
        st.session_state.openai_error = str(e)
        return None

def main():
    """Main application logic."""
    
    # Header
    st.title("🏢 Multi-Domain Intelligence Platform")
    
    # Initialize OpenAI on first run
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = initialize_openai()
    
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
            
            # OpenAI status
            if st.session_state.openai_available:
                st.success("✅ OpenAI Available")
            else:
                st.warning("⚠️ OpenAI Not Available")
                if st.session_state.openai_error:
                    with st.expander("Error Details"):
                        st.error(st.session_state.openai_error)
            
            if st.button("🚪 Logout"):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
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
        from pages.dashboard import main as dashboard_main
        dashboard_main()
    except ImportError:
        st.info("Loading dashboard...")
        show_simple_dashboard()
    except Exception as e:
        st.error(f"Could not load dashboard: {str(e)}")
        st.info("Using simplified dashboard view...")
        show_simple_dashboard()

def show_login_redirect():
    """Redirect to login page."""
    st.info("🔐 Please log in to continue")
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
        
        # OpenAI integration example for cybersecurity
        if st.session_state.openai_available and st.session_state.openai_client:
            st.markdown("### AI Security Analysis")
            security_query = st.text_area("Describe a security concern:", height=100)
            if st.button("Analyze with AI") and security_query:
                with st.spinner("Analyzing..."):
                    try:
                        response = st.session_state.openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a cybersecurity expert."},
                                {"role": "user", "content": security_query}
                            ],
                            max_tokens=300
                        )
                        st.markdown("#### Analysis:")
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
        else:
            st.info("Configure OpenAI API key to enable AI security analysis")
            if st.button("🔄 Retry OpenAI Connection"):
                st.session_state.openai_client = initialize_openai()
                st.rerun()
        
    with tab2:
        st.write("Data Science dashboard would appear here")
        st.info("Sample data analytics")
        
    with tab3:
        st.write("IT Operations dashboard would appear here")
        st.info("Sample IT metrics")

if __name__ == "__main__":
    main()