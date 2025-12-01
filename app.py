"""
Main Entry Point - Multi-Domain Intelligence Platform
"""

import streamlit as st
import os
import sys

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
if 'openai_available' not in st.session_state:
    st.session_state.openai_available = False
if 'openai_error' not in st.session_state:
    st.session_state.openai_error = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"

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
        
        # Simple initialization
        client = OpenAI(api_key=api_key)
        
        # Test the connection with a simple call
        try:
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
    
    # Initialize OpenAI on first run
    if st.session_state.openai_client is None:
        st.session_state.openai_client = initialize_openai()
    
    # Sidebar - Always visible
    with st.sidebar:
        st.markdown("## 🔍 Navigation")
        
        if st.session_state.logged_in:
            st.success(f"Welcome, {st.session_state.username}!")
            
            # OpenAI status
            if st.session_state.openai_available:
                st.success("✅ OpenAI Connected")
                if st.button("🔄 Test OpenAI"):
                    test_openai_connection()
            else:
                st.warning("⚠️ OpenAI Not Available")
                if st.session_state.openai_error:
                    with st.expander("Error Details"):
                        st.error(st.session_state.openai_error)
                if st.button("🔄 Retry OpenAI Setup"):
                    st.session_state.openai_client = initialize_openai()
                    st.rerun()
            
            # Navigation buttons
            st.markdown("---")
            st.markdown("### Pages")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Home"):
                    st.session_state.current_page = "home"
                    st.rerun()
            with col2:
                if st.button("🚪 Logout"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
                    
            if st.session_state.openai_available:
                st.markdown("### AI Tools")
                if st.button("🤖 AI Assistant"):
                    st.session_state.current_page = "ai_assistant"
                    st.rerun()
                if st.button("🔒 Security Analysis"):
                    st.session_state.current_page = "security_ai"
                    st.rerun()
                if st.button("📊 Data Insights"):
                    st.session_state.current_page = "data_ai"
                    st.rerun()
        else:
            st.info("Please log in to access the platform")
        
        st.markdown("---")
        st.markdown("### Demo Credentials")
        st.code("john_analyst / password123")
    
    # Main content area
    st.title("🏢 Multi-Domain Intelligence Platform")
    
    # Route to correct page
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.current_page == "home":
            show_home_page()
        elif st.session_state.current_page == "ai_assistant":
            show_ai_assistant()
        elif st.session_state.current_page == "security_ai":
            show_security_ai()
        elif st.session_state.current_page == "data_ai":
            show_data_ai()
        else:
            show_home_page()

def test_openai_connection():
    """Test OpenAI connection."""
    if st.session_state.openai_client:
        try:
            with st.spinner("Testing connection..."):
                response = st.session_state.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Say 'Connected successfully'"}],
                    max_tokens=10
                )
                st.success(f"✅ {response.choices[0].message.content}")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

def show_login_page():
    """Show login page."""
    st.subheader("🔐 Login to Access Platform")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=150)
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
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
                    st.session_state.current_page = "home"
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try: john_analyst / password123")

def show_home_page():
    """Show home dashboard."""
    st.success(f"✅ Welcome back, {st.session_state.username}!")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Security Alerts", "12", "3 new")
    with col2:
        st.metric("Data Processes", "156", "8%")
    with col3:
        st.metric("System Health", "98%", "-2%")
    
    # Domain tabs
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["🔒 Cybersecurity", "📊 Data Science", "🖥️ IT Operations"])
    
    with tab1:
        st.subheader("Cybersecurity Overview")
        st.write("Monitor security threats and incidents")
        
        if st.session_state.openai_available:
            if st.button("🔍 Analyze Recent Threats", key="cyber_btn"):
                st.session_state.current_page = "security_ai"
                st.rerun()
        else:
            st.info("Enable OpenAI for AI-powered security analysis")
        
        # Sample data
        st.dataframe({
            "Threat": ["Malware", "Phishing", "DDoS", "Insider"],
            "Severity": ["High", "Medium", "High", "Low"],
            "Status": ["Active", "Contained", "Resolved", "Investigation"]
        })
    
    with tab2:
        st.subheader("Data Science Dashboard")
        st.write("Analyze and visualize data patterns")
        
        if st.session_state.openai_available:
            if st.button("📈 Generate Insights", key="data_btn"):
                st.session_state.current_page = "data_ai"
                st.rerun()
        
        # Sample chart
        chart_data = {"Metric": ["Accuracy", "Precision", "Recall", "F1-Score"],
                     "Value": [0.92, 0.89, 0.94, 0.91]}
        st.bar_chart(chart_data, x="Metric", y="Value")
    
    with tab3:
        st.subheader("IT Operations")
        st.write("Monitor system performance and infrastructure")
        
        # System status
        st.progress(85, text="System Load: 85%")
        st.progress(92, text="Network Uptime: 92%")
        st.progress(78, text="Storage Usage: 78%")

def show_ai_assistant():
    """Show AI Assistant page."""
    st.title("🤖 AI Assistant")
    
    if not st.session_state.openai_available:
        st.warning("OpenAI is not available. Please check your API key.")
        return
    
    # Chat interface
    if 'ai_messages' not in st.session_state:
        st.session_state.ai_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Display chat history
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": m["role"], "content": m["content"]} 
                                 for m in st.session_state.ai_messages],
                        max_tokens=500
                    )
                    ai_response = response.choices[0].message.content
                    st.write(ai_response)
                    st.session_state.ai_messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.ai_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
        st.rerun()

def show_security_ai():
    """Show Security AI Analysis page."""
    st.title("🔒 AI Security Analysis")
    
    if not st.session_state.openai_available:
        st.warning("OpenAI is not available for security analysis.")
        return
    
    st.write("Describe a security incident or concern for AI analysis:")
    
    # Input for security analysis
    security_query = st.text_area("Security Issue Description:", 
                                 placeholder="E.g., 'We detected unauthorized access attempts from IP 192.168.1.100...'",
                                 height=150)
    
    analysis_type = st.selectbox("Analysis Type:", 
                                ["Threat Assessment", "Incident Response", "Vulnerability Analysis", 
                                 "Compliance Check", "General Security Advice"])
    
    if st.button("Analyze with AI") and security_query:
        with st.spinner(f"Performing {analysis_type}..."):
            try:
                system_prompt = f"""You are a cybersecurity expert specializing in {analysis_type}. 
                Analyze the security issue and provide:
                1. Risk assessment (Low/Medium/High/Critical)
                2. Immediate actions to take
                3. Long-term prevention strategies
                4. Relevant compliance considerations
                
                Be concise but thorough."""
                
                response = st.session_state.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": security_query}
                    ],
                    max_tokens=800
                )
                
                analysis = response.choices[0].message.content
                
                # Display results
                st.markdown("### 🔍 AI Security Analysis")
                st.markdown("---")
                st.write(analysis)
                
                # Export option
                if st.button("📋 Copy Analysis to Clipboard"):
                    st.code(analysis, language="markdown")
                    st.success("Analysis copied to clipboard format!")
                    
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
    
    # Example queries
    with st.expander("💡 Example Security Queries"):
        st.write("""
        - "Multiple failed login attempts detected on admin account"
        - "Suspicious network traffic from external IPs"
        - "Employee reported phishing email asking for credentials"
        - "Need to assess GDPR compliance for our data handling"
        - "Planning incident response for ransomware attack"
        """)

def show_data_ai():
    """Show Data Science AI Insights page."""
    st.title("📊 AI Data Insights")
    
    if not st.session_state.openai_available:
        st.warning("OpenAI is not available for data analysis.")
        return
    
    st.write("Ask questions about your data or request analysis:")
    
    # Data analysis options
    data_query = st.text_input("Your data question:", 
                              placeholder="E.g., 'What trends should I look for in sales data?'")
    
    data_context = st.text_area("Provide context about your data (optional):",
                               placeholder="E.g., 'I have monthly sales data for 2023 with columns: date, product, revenue, region'",
                               height=100)
    
    analysis_goal = st.selectbox("Analysis Goal:",
                                ["Trend Identification", "Anomaly Detection", "Predictive Insights",
                                 "Pattern Recognition", "Optimization Suggestions", "Correlation Analysis"])
    
    if st.button("Generate Insights") and data_query:
        with st.spinner("Analyzing data patterns..."):
            try:
                system_prompt = f"""You are a data science expert. The user wants {analysis_goal}.
                Provide actionable insights including:
                1. Key findings and patterns
                2. Statistical recommendations
                3. Visualization suggestions
                4. Next steps for deeper analysis
                
                Context about the data: {data_context if data_context else 'No specific context provided'}"""
                
                response = st.session_state.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": data_query}
                    ],
                    max_tokens=700
                )
                
                insights = response.choices[0].message.content
                
                # Display results
                st.markdown("### 📈 AI Data Insights")
                st.markdown("---")
                st.write(insights)
                
                # Visual suggestions
                st.markdown("#### 📊 Recommended Visualizations:")
                viz_col1, viz_col2, viz_col3 = st.columns(3)
                with viz_col1:
                    st.metric("Line Chart", "Trends", "Recommended")
                with viz_col2:
                    st.metric("Heatmap", "Correlations", "Useful")
                with viz_col3:
                    st.metric("Scatter Plot", "Relationships", "Consider")
                    
            except Exception as e:
                st.error(f"Insight generation failed: {str(e)}")
    
    # Quick analysis templates
    with st.expander("🚀 Quick Analysis Templates"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sales Trends"):
                st.session_state.current_page = "ai_assistant"
                st.rerun()
        with col2:
            if st.button("User Behavior"):
                st.session_state.current_page = "ai_assistant"
                st.rerun()

if __name__ == "__main__":
    main()