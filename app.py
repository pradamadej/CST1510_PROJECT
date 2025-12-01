"""
Multi-Domain Intelligence Platform - Error Safe Version
"""

import streamlit as st
import os

# Set page config - MUST BE FIRST
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🏢",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'openai_client' not in st.session_state:
    st.session_state.openai_client = None
if 'openai_status' not in st.session_state:
    st.session_state.openai_status = "not_configured"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'plotly_available' not in st.session_state:
    st.session_state.plotly_available = False

def setup_openai():
    """Simple OpenAI setup without proxies parameter"""
    try:
        # Get API key
        api_key = None
        
        # Check Streamlit secrets
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
                st.session_state.openai_status = "found_in_secrets"
        except:
            pass
        
        # Check environment
        if not api_key:
            api_key = os.environ.get('OPENAI_API_KEY')
            if api_key:
                st.session_state.openai_status = "found_in_env"
        
        # No key found
        if not api_key:
            st.session_state.openai_status = "no_key"
            return None
        
        # Clean key
        api_key = api_key.strip()
        
        # Import and create client
        try:
            import openai
            
            # VERSION CHECK
            openai_version = openai.__version__
            
            if openai_version.startswith('1.'):
                client = openai.OpenAI(api_key=api_key)
                st.session_state.openai_status = f"connected_v{openai_version}"
                return client
            else:
                openai.api_key = api_key
                st.session_state.openai_status = f"connected_v{openai_version}_legacy"
                return openai
                
        except ImportError:
            st.session_state.openai_status = "not_installed"
            return None
            
    except Exception as e:
        st.session_state.openai_status = f"error: {str(e)}"
        return None

def check_plotly():
    """Check if plotly is available"""
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        st.session_state.plotly_available = True
        return True
    except ImportError:
        st.session_state.plotly_available = False
        return False

def test_openai():
    """Test OpenAI connection"""
    client = setup_openai()
    
    if not client:
        return False, "No client"
    
    try:
        if hasattr(client, 'chat'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=10
            )
            return True, response.choices[0].message.content
        else:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=10
            )
            return True, response.choices[0].message.content
            
    except Exception as e:
        return False, str(e)

def main():
    """Main app"""
    
    # Check plotly on startup
    if not st.session_state.plotly_available:
        check_plotly()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔍 Navigation")
        
        if st.session_state.logged_in:
            st.success(f"Welcome, {st.session_state.username}!")
            
            # Status indicators
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.openai_status.startswith("connected"):
                    st.success("🤖 AI")
                else:
                    st.error("🤖 AI")
            with col2:
                if st.session_state.plotly_available:
                    st.success("📊 Charts")
                else:
                    st.error("📊 Charts")
            
            # Navigation
            st.markdown("---")
            pages = [
                ("🏠 Home", "home"),
                ("🤖 AI Chat", "chat"),
                ("📊 Dashboard", "dashboard"),
                ("⚙️ Settings", "settings")
            ]
            
            for page_name, page_id in pages:
                if st.button(page_name, key=f"nav_{page_id}"):
                    st.session_state.current_page = page_id
                    st.rerun()
                
            st.markdown("---")
            if st.button("🚪 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
                
        else:
            st.info("Please login")
            st.markdown("---")
            st.markdown("**Demo Credentials:**")
            st.code("john_analyst / password123")
    
    # Main content
    st.title("🏢 Intelligence Platform")
    
    if not st.session_state.logged_in:
        show_login()
    else:
        if st.session_state.current_page == "home":
            show_home()
        elif st.session_state.current_page == "chat":
            show_chat()
        elif st.session_state.current_page == "dashboard":
            show_dashboard_safe()
        elif st.session_state.current_page == "settings":
            show_settings()
        else:
            show_home()

def show_login():
    """Login page"""
    st.subheader("🔐 Login")
    
    with st.form("login"):
        user = st.text_input("Username", value="john_analyst")
        pwd = st.text_input("Password", type="password", value="password123")
        
        if st.form_submit_button("Login"):
            if user == "john_analyst" and pwd == "password123":
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error("Use: john_analyst / password123")

def show_home():
    """Home page"""
    st.success("✅ Dashboard")
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Alerts", "12")
    with col2:
        st.metric("Processes", "156")
    with col3:
        st.metric("Health", "98%")
    
    st.markdown("---")
    
    # Quick tests
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Test OpenAI"):
            success, msg = test_openai()
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")
    with col2:
        if st.button("Check Plotly"):
            if check_plotly():
                st.success("✅ Plotly available")
            else:
                st.error("❌ Plotly not installed")

def show_chat():
    """AI Chat page"""
    st.title("🤖 AI Assistant")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    success, response = test_openai()
                    
                    if success:
                        client = setup_openai()
                        if client and hasattr(client, 'chat'):
                            ai_response_obj = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": "You are a helpful assistant."},
                                    {"role": "user", "content": prompt}
                                ],
                                max_tokens=200
                            )
                            ai_response = ai_response_obj.choices[0].message.content
                        else:
                            ai_response = "Connected! How can I help?"
                    else:
                        ai_response = "OpenAI not available. Please check settings."
                    
                    st.write(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

def show_dashboard_safe():
    """Safe dashboard that won't crash"""
    st.title("📊 Dashboard")
    
    # Check if we should try to load external dashboard
    if st.session_state.plotly_available:
        try:
            # Try to import and run the dashboard
            import importlib.util
            import sys
            
            # Check if dashboard module exists
            dashboard_path = "pages/dashboard.py"
            if os.path.exists(dashboard_path):
                try:
                    # Create a custom import
                    spec = importlib.util.spec_from_file_location("dashboard", dashboard_path)
                    dashboard_module = importlib.util.module_from_spec(spec)
                    sys.modules["dashboard"] = dashboard_module
                    
                    # Read and execute the code with error handling
                    with open(dashboard_path, 'r') as f:
                        code = f.read()
                    
                    # Replace set_page_config calls to avoid errors
                    code = code.replace('st.set_page_config', '# st.set_page_config')
                    
                    # Execute in a safe namespace
                    exec_globals = {'st': st, 'plotly': None}
                    exec(code, exec_globals)
                    
                    # Try to call main if it exists
                    if 'main' in exec_globals:
                        exec_globals['main']()
                    else:
                        st.info("Dashboard loaded but no main() function found")
                        
                except Exception as e:
                    st.error(f"Error loading dashboard: {str(e)}")
                    show_fallback_dashboard()
            else:
                st.info("No external dashboard found")
                show_fallback_dashboard()
                
        except Exception as e:
            st.error(f"Dashboard error: {str(e)}")
            show_fallback_dashboard()
    else:
        st.warning("⚠️ Plotly not installed. Using simplified dashboard.")
        show_fallback_dashboard()

def show_fallback_dashboard():
    """Fallback dashboard when plotly is not available"""
    st.info("Using simplified dashboard view")
    
    # Tabs for different domains
    tab1, tab2, tab3 = st.tabs(["🔒 Security", "📈 Analytics", "🖥️ Operations"])
    
    with tab1:
        st.subheader("Security Overview")
        
        # Security metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Threats", "12", "+2")
        with col2:
            st.metric("Incidents", "3", "0")
        with col3:
            st.metric("Blocked", "156", "+24")
        
        # Security log
        st.markdown("### Recent Events")
        events = [
            {"Time": "10:30", "Event": "Failed login", "Severity": "Medium"},
            {"Time": "11:15", "Event": "Port scan", "Severity": "High"},
            {"Time": "12:45", "Event": "Policy update", "Severity": "Low"},
        ]
        st.table(events)
    
    with tab2:
        st.subheader("Data Analytics")
        
        # Simple data display
        import pandas as pd
        import numpy as np
        
        # Generate sample data
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.randint(100, 1000, 30),
            'Users': np.random.randint(50, 500, 30),
            'Engagement': np.random.rand(30) * 100
        })
        
        st.dataframe(data)
        
        # Simple line chart using streamlit
        st.line_chart(data.set_index('Date')[['Sales', 'Users']])
    
    with tab3:
        st.subheader("IT Operations")
        
        # System metrics
        st.progress(0.85, text="CPU Usage: 85%")
        st.progress(0.92, text="Memory: 92%")
        st.progress(0.64, text="Disk: 64%")
        st.progress(0.99, text="Network: 99%")
        
        # System status
        st.markdown("### Service Status")
        services = {
            "Web Server": "✅ Running",
            "Database": "✅ Running", 
            "API Gateway": "⚠️ Slow",
            "Cache": "✅ Running",
            "Monitoring": "✅ Running"
        }
        
        for service, status in services.items():
            st.write(f"- **{service}:** {status}")

def show_settings():
    """Settings page"""
    st.title("⚙️ Settings")
    
    # OpenAI Configuration
    st.markdown("### 🤖 OpenAI Configuration")
    
    # Current status
    status_color = "🟢" if st.session_state.openai_status.startswith("connected") else "🔴"
    st.info(f"**Status:** {status_color} {st.session_state.openai_status}")
    
    # API Key input
    api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
    
    if st.button("Save & Test API Key"):
        if api_key:
            # Save temporarily
            os.environ['OPENAI_API_KEY'] = api_key
            st.session_state.openai_client = None
            
            # Test
            success, msg = test_openai()
            if success:
                st.success(f"✅ {msg}")
                st.rerun()
            else:
                st.error(f"❌ {msg}")
        else:
            st.warning("Please enter an API key")
    
    # Dependencies Status
    st.markdown("---")
    st.markdown("### 📦 Dependencies")
    
    deps = [
        ("Streamlit", "streamlit", "1.36.0"),
        ("OpenAI", "openai", "1.6.1"),
        ("Plotly", "plotly", "5.18.0"),
        ("Python-dotenv", "python-dotenv", "1.0.0"),
    ]
    
    for dep_name, dep_module, expected_ver in deps:
        try:
            module = __import__(dep_module)
            version = getattr(module, '__version__', 'Unknown')
            status = "✅" if version == expected_ver else f"⚠️ {version}"
            st.write(f"- **{dep_name}:** {status}")
        except ImportError:
            st.write(f"- **{dep_name}:** ❌ Not installed")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📝 Setup Instructions")
    
    st.markdown("""
    1. **Add to Streamlit Secrets:**
       ```toml
       OPENAI_API_KEY = "sk-your-key-here"
       ```
    
    2. **Required packages in requirements.txt:**
       ```txt
       streamlit==1.36.0
       openai==1.6.1
       python-dotenv==1.0.0
       plotly==5.18.0
       ```
    
    3. **Test connection** using the button above
    """)

if __name__ == "__main__":
    main()