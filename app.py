"""
Multi-Domain Intelligence Platform - Main Application
Secure, robust version with all fixes applied
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Set page config - MUST BE FIRST
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize ALL session state variables at the top
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'openai_client' not in st.session_state:
    st.session_state.openai_client = None
if 'openai_available' not in st.session_state:
    st.session_state.openai_available = False
if 'openai_error' not in st.session_state:
    st.session_state.openai_error = ""
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'last_activity' not in st.session_state:
    st.session_state.last_activity = datetime.now()

# OpenAI setup function - SIMPLIFIED AND FIXED
def get_openai_client():
    """Get OpenAI client if API key is available"""
    try:
        # Return existing client if available
        if st.session_state.openai_client is not None:
            return st.session_state.openai_client
        
        # Get API key from secrets or environment
        api_key = None
        
        # Method 1: Streamlit secrets (for cloud)
        try:
            if hasattr(st, 'secrets'):
                api_key = st.secrets.get("OPENAI_API_KEY", "")
        except:
            pass
        
        # Method 2: Environment variable
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY", "")
        
        # Check if key exists and is valid
        if not api_key or not api_key.strip():
            st.session_state.openai_error = "No API key found"
            return None
        
        api_key = api_key.strip()
        
        if not api_key.startswith("sk-"):
            st.session_state.openai_error = "Invalid API key format (should start with 'sk-')"
            return None
        
        # Import OpenAI - handle different versions
        try:
            from openai import OpenAI
            
            # Create simple client without extra parameters
            client = OpenAI(api_key=api_key)
            
            # Test connection with timeout
            import requests
            import socket
            socket.setdefaulttimeout(10)
            
            # Simple test
            test_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'OK'"}],
                max_tokens=5,
                timeout=10
            )
            
            if test_response.choices[0].message.content:
                st.session_state.openai_client = client
                st.session_state.openai_available = True
                st.session_state.openai_error = "Connected successfully"
                return client
            else:
                st.session_state.openai_error = "Test response empty"
                return None
                
        except ImportError:
            st.session_state.openai_error = "OpenAI package not installed"
            return None
        except Exception as e:
            st.session_state.openai_error = f"Connection failed: {str(e)}"
            return None
            
    except Exception as e:
        st.session_state.openai_error = f"Setup error: {str(e)}"
        return None

def test_openai_connection():
    """Test OpenAI connection and update status"""
    client = get_openai_client()
    
    if client:
        try:
            # Quick test
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Connected' if working."}],
                max_tokens=10,
                timeout=5
            )
            
            st.session_state.openai_available = True
            st.session_state.openai_error = "✅ Connected"
            return True, response.choices[0].message.content
            
        except Exception as e:
            st.session_state.openai_available = False
            st.session_state.openai_error = f"❌ Test failed: {str(e)}"
            return False, str(e)
    
    return False, "No client available"

def main():
    """Main application logic"""
    
    # Update last activity timestamp
    st.session_state.last_activity = datetime.now()
    
    # Initialize OpenAI on first load
    if st.session_state.openai_client is None:
        get_openai_client()
    
    # Sidebar - Always visible
    with st.sidebar:
        st.markdown("# 🔍 Navigation")
        
        if st.session_state.logged_in:
            # User info
            st.success(f"👤 {st.session_state.username}")
            st.caption(f"Role: {st.session_state.user_role}")
            
            # OpenAI status
            st.markdown("### 🤖 AI Status")
            
            if st.session_state.openai_available:
                st.success("✅ OpenAI Connected")
                if st.button("Test AI", key="sidebar_test_ai"):
                    success, message = test_openai_connection()
                    if success:
                        st.success(f"Response: {message}")
                    else:
                        st.error(f"Error: {message}")
                    st.rerun()
            else:
                st.error("❌ OpenAI Offline")
                if st.session_state.openai_error:
                    with st.expander("Details"):
                        st.error(st.session_state.openai_error)
                
                if st.button("Retry Connection", key="sidebar_retry"):
                    st.session_state.openai_client = None
                    get_openai_client()
                    st.rerun()
            
            st.markdown("---")
            
            # Page navigation
            st.markdown("### 🗂️ Menu")
            
            menu_items = [
                ("🏠 Home", "home"),
                ("📊 Dashboard", "dashboard"),
                ("🤖 AI Assistant", "assistant"),
                ("🔒 Security Tools", "security"),
                ("📈 Analytics", "analytics"),
                ("⚙️ Settings", "settings")
            ]
            
            for item_name, item_id in menu_items:
                if st.button(item_name, key=f"menu_{item_id}", use_container_width=True):
                    st.session_state.current_page = item_id
                    st.rerun()
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                # Clear all session data
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("Logged out successfully!")
                st.rerun()
                
        else:
            # Not logged in view
            st.info("🔐 Please login to continue")
            st.markdown("---")
            st.markdown("### Demo Credentials")
            st.code("""
            Username: john_analyst
            Password: password123
            
            Other users:
            - sara_scientist
            - mike_admin
            """)
            
            # Direct login button
            if st.button("Go to Login", type="secondary", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
    
    # Main content area
    st.title("🏢 Multi-Domain Intelligence Platform")
    
    # Page routing with authentication check
    if not st.session_state.logged_in:
        # Only show login page if not logged in
        show_login_page()
    else:
        # User is logged in - show appropriate page
        if st.session_state.current_page == "home":
            show_home_page()
        elif st.session_state.current_page == "dashboard":
            show_dashboard_page()
        elif st.session_state.current_page == "assistant":
            show_assistant_page()
        elif st.session_state.current_page == "security":
            show_security_page()
        elif st.session_state.current_page == "analytics":
            show_analytics_page()
        elif st.session_state.current_page == "settings":
            show_settings_page()
        elif st.session_state.current_page == "login":
            # If logged in but on login page, redirect to home
            st.session_state.current_page = "home"
            st.rerun()
        else:
            show_home_page()

def show_login_page():
    """Login page - shown when user is not logged in"""
    st.subheader("🔐 Login Required")
    
    # Clear any existing errors
    if 'login_error' in st.session_state:
        del st.session_state.login_error
    
    # Login form
    with st.form("login_form"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=100)
        
        with col2:
            st.markdown("### Welcome Back")
            st.markdown("Enter your credentials to continue")
        
        username = st.text_input("Username", value="john_analyst", placeholder="Enter username")
        password = st.text_input("Password", type="password", value="password123", placeholder="Enter password")
        
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submit:
            # Simple authentication (can be replaced with bcrypt or database check)
            demo_users = {
                'john_analyst': {'password': 'password123', 'role': 'analyst'},
                'sara_scientist': {'password': 'password123', 'role': 'scientist'},
                'mike_admin': {'password': 'password123', 'role': 'admin'},
                'Joel_analyst': {'password': 'password123', 'role': 'analyst'},
                'Sara_scientist': {'password': 'password123', 'role': 'scientist'},
                'Daniel_admin': {'password': 'password123', 'role': 'admin'}
            }
            
            if username in demo_users and password == demo_users[username]['password']:
                # Login successful
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = demo_users[username]['role']
                st.session_state.current_page = "home"
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try: john_analyst / password123")
    
    # Quick login buttons
    st.markdown("---")
    st.markdown("### Quick Login (Demo)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍💻 John (Analyst)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "john_analyst"
            st.session_state.user_role = "analyst"
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("👩‍🔬 Sara (Scientist)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "sara_scientist"
            st.session_state.user_role = "scientist"
            st.session_state.current_page = "home"
            st.rerun()
    
    with col3:
        if st.button("👨‍💼 Mike (Admin)", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.username = "mike_admin"
            st.session_state.user_role = "admin"
            st.session_state.current_page = "home"
            st.rerun()

def show_home_page():
    """Home page - main dashboard view"""
    st.success(f"✅ Welcome back, {st.session_state.username}!")
    
    # Quick stats
    st.markdown("## 📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users", "24", "+3")
        st.caption("Online now")
    
    with col2:
        st.metric("Security Score", "94%", "+2%")
        st.caption("Threats blocked")
    
    with col3:
        st.metric("Data Processes", "187", "+24")
        st.caption("Today")
    
    with col4:
        st.metric("System Health", "98%", "-1%")
        st.caption("Uptime")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Go to Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    with col2:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.current_page = "assistant"
            st.rerun()
    
    with col3:
        if st.button("🔒 Security Scan", use_container_width=True):
            st.info("Security scan initiated...")
    
    # Recent activity
    st.markdown("---")
    st.markdown("## 📋 Recent Activity")
    
    activity_data = {
        "Time": ["10:30", "11:15", "12:45", "14:20"],
        "User": ["john_analyst", "sara_scientist", "mike_admin", st.session_state.username],
        "Action": ["Login", "Data Analysis", "System Update", "Dashboard Access"],
        "Status": ["Success", "Completed", "In Progress", "Success"]
    }
    
    import pandas as pd
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(activity_df, use_container_width=True, hide_index=True)
    
    # AI Status
    if st.session_state.openai_available:
        st.markdown("---")
        st.markdown("## 🤖 AI Status: Online")
        
        # Quick AI test
        if st.button("Quick AI Test", key="home_ai_test"):
            with st.spinner("Testing AI..."):
                success, message = test_openai_connection()
                if success:
                    st.success(f"✅ AI Response: {message}")
                else:
                    st.error(f"❌ AI Error: {message}")

def show_dashboard_page():
    """Dashboard page - uses pages/dashboard.py if available, otherwise shows built-in"""
    
    # SECURITY CHECK: Ensure user is logged in
    if not st.session_state.logged_in:
        st.error("🔒 Access Denied")
        st.warning("You must be logged in to access the dashboard.")
        show_login_page()
        return
    
    try:
        # Try to import and show the external dashboard
        from pages.dashboard import main as dashboard_main
        dashboard_main()
    except ImportError:
        # Fallback: Show built-in dashboard
        show_fallback_dashboard()
    except Exception as e:
        st.error(f"Dashboard error: {str(e)}")
        show_fallback_dashboard()

def show_fallback_dashboard():
    """Fallback dashboard when external one fails"""
    st.title("📊 Dashboard")
    st.success(f"Welcome, {st.session_state.username}!")
    
    # Simple dashboard content
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Your Role", st.session_state.user_role)
        st.metric("Session Time", "45m")
    
    with col2:
        st.metric("Today's Actions", "28")
        st.metric("Last Login", "Today")
    
    st.markdown("---")
    
    # Quick navigation
    st.markdown("### Quick Navigation")
    
    if st.button("🔒 Security Tools"):
        st.session_state.current_page = "security"
        st.rerun()
    
    if st.button("📈 Analytics"):
        st.session_state.current_page = "analytics"
        st.rerun()
    
    if st.button("⚙️ Settings"):
        st.session_state.current_page = "settings"
        st.rerun()

def show_assistant_page():
    """AI Assistant page"""
    
    # SECURITY CHECK
    if not st.session_state.logged_in:
        st.error("Access denied. Please log in first.")
        return
    
    st.title("🤖 AI Assistant")
    
    if not st.session_state.openai_available:
        st.warning("⚠️ OpenAI not available")
        st.info("Please configure your API key in Settings to use AI features.")
        
        if st.button("Go to Settings"):
            st.session_state.current_page = "settings"
            st.rerun()
        
        return
    
    # Initialize chat history
    if 'assistant_messages' not in st.session_state:
        st.session_state.assistant_messages = [
            {"role": "assistant", "content": f"Hello {st.session_state.username}! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Display chat history
    for message in st.session_state.assistant_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask {st.session_state.username}'s AI assistant..."):
        # Add user message
        st.session_state.assistant_messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("▌")
            
            try:
                client = get_openai_client()
                
                if not client:
                    st.error("AI service unavailable")
                    return
                
                # Create completion
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.assistant_messages,
                    max_tokens=300
                )
                
                # Get response
                full_response = response.choices[0].message.content
                
                # Display response
                message_placeholder.markdown(full_response)
                
                # Add to history
                st.session_state.assistant_messages.append(
                    {"role": "assistant", "content": full_response}
                )
                
            except Exception as e:
                error_msg = f"⚠️ Error: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.assistant_messages.append(
                    {"role": "assistant", "content": f"I encountered an error: {str(e)}"}
                )
    
    # Clear chat button
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("Clear Chat", type="secondary"):
            st.session_state.assistant_messages = [
                {"role": "assistant", "content": f"Hello {st.session_state.username}! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()

def show_security_page():
    """Security tools page"""
    
    # SECURITY CHECK
    if not st.session_state.logged_in:
        st.error("Access denied. Please log in first.")
        return
    
    st.title("🔒 Security Tools")
    
    # Security tools based on user role
    st.markdown(f"### Security Tools for {st.session_state.username}")
    
    # Role-based tools
    if st.session_state.user_role == 'admin':
        st.success("🛡️ Admin Security Privileges")
        
        tools = [
            ("User Management", "Manage user accounts and permissions"),
            ("Access Logs", "View system access logs"),
            ("Security Config", "Configure security settings"),
            ("Audit Reports", "Generate security audit reports")
        ]
    elif st.session_state.user_role == 'analyst':
        st.info("📋 Analyst Security Tools")
        
        tools = [
            ("Threat Analysis", "Analyze security threats"),
            ("Incident Reports", "View and create incident reports"),
            ("Access Review", "Review user access patterns"),
            ("Security Dashboard", "View security metrics")
        ]
    else:
        st.warning("👀 Viewer Security Access")
        
        tools = [
            ("Security Status", "View current security status"),
            ("Alerts", "View security alerts"),
            ("Guidelines", "Security guidelines and policies")
        ]
    
    # Display tools
    for tool_name, tool_desc in tools:
        with st.expander(f"🔧 {tool_name}"):
            st.write(tool_desc)
            if st.button(f"Open {tool_name}", key=f"security_{tool_name}"):
                st.info(f"Opening {tool_name}...")

def show_analytics_page():
    """Analytics page"""
    
    # SECURITY CHECK
    if not st.session_state.logged_in:
        st.error("Access denied. Please log in first.")
        return
    
    st.title("📈 Analytics")
    
    # Analytics tools
    st.markdown(f"### Analytics for {st.session_state.username}")
    
    # Sample analytics
    import pandas as pd
    import numpy as np
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    analytics_data = pd.DataFrame({
        'Date': dates,
        'Users': np.random.randint(10, 50, 30),
        'Processes': np.random.randint(50, 200, 30),
        'Errors': np.random.randint(0, 10, 30),
        'Success Rate': np.random.randint(85, 100, 30)
    })
    
    # Display data
    st.dataframe(analytics_data, use_container_width=True)
    
    # Charts
    st.markdown("### Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.line_chart(analytics_data.set_index('Date')[['Users', 'Processes']])
    
    with col2:
        st.line_chart(analytics_data.set_index('Date')[['Success Rate']])

def show_settings_page():
    """Settings page"""
    
    # SECURITY CHECK
    if not st.session_state.logged_in:
        st.error("Access denied. Please log in first.")
        return
    
    st.title("⚙️ Settings")
    
    # User settings
    st.markdown("### 👤 User Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Username:** {st.session_state.username}")
        st.info(f"**Role:** {st.session_state.user_role}")
        st.info(f"**Session Started:** {st.session_state.last_activity.strftime('%H:%M')}")
    
    with col2:
        # Theme selector
        theme = st.selectbox("Theme", ["Light", "Dark", "System"])
        
        # Notifications
        notifications = st.checkbox("Enable notifications", True)
        
        if st.button("Save Preferences"):
            st.success("Preferences saved!")
    
    # OpenAI settings
    st.markdown("---")
    st.markdown("### 🤖 OpenAI Configuration")
    
    # Current status
    if st.session_state.openai_available:
        st.success("✅ OpenAI is connected")
    else:
        st.error("❌ OpenAI is not configured")
    
    # API Key input
    st.subheader("API Key Configuration")
    
    api_key = st.text_input(
        "OpenAI API Key:",
        type="password",
        placeholder="sk-...",
        help="Enter your OpenAI API key starting with 'sk-'"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Test Connection", use_container_width=True):
            if api_key:
                # Temporarily set key
                os.environ['OPENAI_API_KEY'] = api_key
                # Reset client
                st.session_state.openai_client = None
                # Test
                success, message = test_openai_connection()
                if success:
                    st.success(f"✅ Connected: {message}")
                else:
                    st.error(f"❌ Failed: {message}")
            else:
                st.warning("Please enter an API key first")
    
    with col2:
        if st.button("Reset AI", use_container_width=True):
            st.session_state.openai_client = None
            st.session_state.openai_available = False
            st.session_state.openai_error = "Reset - configure API key"
            st.success("AI settings reset")
            st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("📖 Setup Instructions"):
        st.markdown("""
        1. **Get API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
        2. **For Streamlit Cloud:** Add to Settings → Secrets:
           ```toml
           OPENAI_API_KEY = "sk-your-key-here"
           ```
        3. **Test connection** using the button above
        """)
    
    # System info
    st.markdown("---")
    with st.expander("🖥️ System Information"):
        st.write(f"**Streamlit:** {st.__version__}")
        st.write(f"**Python:** {sys.version.split()[0]}")
        
        try:
            import pandas as pd
            st.write(f"**Pandas:** {pd.__version__}")
        except:
            st.write("**Pandas:** Not available")
        
        try:
            import openai
            st.write(f"**OpenAI:** {openai.__version__}")
        except:
            st.write("**OpenAI:** Not available")

if __name__ == "__main__":
    main()