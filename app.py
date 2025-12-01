"""
Main Entry Point - Multi-Domain Intelligence Platform
"""

import streamlit as st
from openai import OpenAI
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
if 'openai_client' not in st.session_state:
    st.session_state.openai_client = None

def initialize_openai():
    """Initialize OpenAI client with API key from secrets."""
    try:
        # Get API key from Streamlit secrets (for cloud) or environment variable
        api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
        
        if not api_key:
            st.warning("OpenAI API key not found. Some features may be limited.")
            return None
        
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI: {str(e)}")
        return None

def main():
    """Main application logic."""
    
    # Header
    st.title("🏢 Multi-Domain Intelligence Platform")
    
    # Initialize OpenAI client if not already done
    if st.session_state.openai_client is None:
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
            if st.session_state.openai_client:
                st.success("✅ OpenAI Connected")
            else:
                st.warning("⚠️ OpenAI Not Configured")
            
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.session_state.openai_client = None
                st.rerun()
        else:
            st.info("Please log in to access the platform")
        
        st.markdown("---")
        st.markdown("### Demo Credentials")
        st.code("Username: john_analyst\nPassword: password123")
        
        # Test OpenAI connection button
        if st.session_state.logged_in and st.session_state.openai_client:
            if st.button("🔧 Test OpenAI Connection"):
                test_openai_connection()

def test_openai_connection():
    """Test the OpenAI connection."""
    try:
        with st.spinner("Testing OpenAI connection..."):
            client = st.session_state.openai_client
            # Make a simple request to test
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Say 'Connection successful' if you can read this."}
                ],
                max_tokens=10
            )
            if response.choices[0].message.content:
                st.success(f"✅ OpenAI Connection Successful!")
                st.info(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        st.error(f"❌ OpenAI Connection Failed: {str(e)}")

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
        
        # OpenAI integration example for cybersecurity
        if st.session_state.openai_client:
            st.markdown("### AI Security Analysis")
            security_query = st.text_area("Describe a security concern:", height=100)
            if st.button("Analyze with AI") and security_query:
                analyze_security_issue(security_query)
        else:
            st.info("Connect OpenAI API to enable AI security analysis")
        
    with tab2:
        st.write("Data Science dashboard would appear here")
        
        # OpenAI integration example for data science
        if st.session_state.openai_client:
            st.markdown("### AI Data Insights")
            data_question = st.text_input("Ask about your data:")
            if st.button("Get AI Insights") and data_question:
                get_data_insights(data_question)
        
    with tab3:
        st.write("IT Operations dashboard would appear here")
        st.info("Sample IT metrics")

def analyze_security_issue(query):
    """Analyze security issues using OpenAI."""
    try:
        with st.spinner("Analyzing security issue..."):
            client = st.session_state.openai_client
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert. Analyze the security concern and provide recommendations."},
                    {"role": "user", "content": query}
                ],
                max_tokens=500
            )
            
            st.markdown("### AI Security Analysis Result:")
            st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error analyzing security issue: {str(e)}")

def get_data_insights(question):
    """Get data science insights using OpenAI."""
    try:
        with st.spinner("Generating insights..."):
            client = st.session_state.openai_client
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data science expert. Provide insights and analysis for data-related questions."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            
            st.markdown("### AI Data Insights:")
            st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error generating insights: {str(e)}")

if __name__ == "__main__":
    main()