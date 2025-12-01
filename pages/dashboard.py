"""
Dashboard Page - Updated for OpenAI 0.28.1
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Check login
if not st.session_state.get('logged_in'):
    st.error("Please log in first")
    st.stop()

# AI Assistant class for OpenAI 0.28.1
class AIAssistant:
    def __init__(self):
        self.api_key = st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, 'secrets') else ""
    
    def get_response(self, prompt, context=""):
        """Get AI response using OpenAI 0.28.1"""
        if not self.api_key:
            return "API key not configured"
        
        try:
            import openai
            
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{context}\n\n{prompt}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Error: {str(e)}"

def main():
    """Main dashboard function."""
    
    # Header
    st.title(f"📊 Welcome, {st.session_state.username}!")
    st.markdown(f"**Role:** {st.session_state.get('user_role', 'User')}")
    
    # Initialize AI
    ai = AIAssistant()
    
    # Domain selection
    domain = st.sidebar.selectbox(
        "Select Domain",
        ["Cybersecurity", "Data Science", "IT Operations", "AI Assistant"]
    )
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()
    
    # Domain content
    if domain == "Cybersecurity":
        show_cybersecurity()
    elif domain == "Data Science":
        show_data_science()
    elif domain == "IT Operations":
        show_it_operations()
    elif domain == "AI Assistant":
        show_ai_assistant(ai)

def show_cybersecurity():
    """Cybersecurity dashboard."""
    st.header("🔒 Cybersecurity Dashboard")
    
    # Sample data
    data = pd.DataFrame({
        'Severity': ['Critical', 'High', 'Medium', 'Low'],
        'Count': [5, 12, 23, 45],
        'Status': ['Open', 'Open', 'In Progress', 'Resolved']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Incidents", 85)
        st.metric("Open Incidents", 17)
        
    with col2:
        st.metric("Critical", 5)
        st.metric("Avg Resolution", "24h")
    
    # Charts
    fig1 = px.pie(data, values='Count', names='Severity', title="Incidents by Severity")
    st.plotly_chart(fig1, use_container_width=True)

def show_data_science():
    """Data Science dashboard."""
    st.header("📊 Data Science Dashboard")
    
    # Sample data
    data = pd.DataFrame({
        'Department': ['Sales', 'Marketing', 'IT', 'Finance', 'HR'],
        'Datasets': [45, 32, 67, 28, 15],
        'Quality': [0.85, 0.92, 0.78, 0.95, 0.88]
    })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Datasets", 187)
    with col2:
        st.metric("Avg Quality", "0.88")
    with col3:
        st.metric("Storage Used", "4.2 GB")
    
    # Charts
    fig1 = px.bar(data, x='Department', y='Datasets', title="Datasets by Department")
    st.plotly_chart(fig1, use_container_width=True)

def show_it_operations():
    """IT Operations dashboard."""
    st.header("🖥️ IT Operations Dashboard")
    
    # Sample data
    data = pd.DataFrame({
        'Priority': ['Urgent', 'High', 'Medium', 'Low'],
        'Count': [8, 15, 42, 30],
        'Status': ['Open', 'In Progress', 'Resolved', 'Closed']
    })
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Open Tickets", 23)
    with col2:
        st.metric("Urgent", 8)
    with col3:
        st.metric("Avg Response", "2.5h")
    
    # Charts
    fig1 = px.bar(data, x='Priority', y='Count', color='Priority', title="Tickets by Priority")
    st.plotly_chart(fig1, use_container_width=True)

def show_ai_assistant(ai):
    """AI Assistant interface."""
    st.header("🤖 AI Assistant")
    
    st.info("Ask questions about your data or get insights")
    
    question = st.text_area("Your question:", height=100)
    
    if st.button("Get AI Analysis"):
        if question:
            with st.spinner("Thinking..."):
                response = ai.get_response(question)
                st.markdown("### AI Response:")
                st.write(response)
        else:
            st.warning("Please enter a question")

if __name__ == "__main__":
    main()