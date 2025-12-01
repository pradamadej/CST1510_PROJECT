"""
Main Dashboard for Multi-Domain Intelligence Platform
File: pages/2_Dashboard.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import json

# Add project root to path for imports
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, proj_root)

# Import DatabaseManager
try:
    # Try importing from the correct location
    from database_manager import DatabaseManager
except ImportError:
    # If database_manager.py is not in project root, try different approach
    st.error("DatabaseManager not found. Please ensure database_manager.py is in the project root.")
    # Create a minimal DatabaseManager class as fallback
    class DatabaseManager:
        def __init__(self, db_name="intelligence_platform.db"):
            self.db_name = db_name
            st.warning(f"Using fallback DatabaseManager with {db_name}")
        
        def execute_query(self, query, params=()):
            return []
        
        def get_cyber_incidents(self, filters=None):
            return []
        
        def get_all_records(self, table_name):
            return []
        
        def close(self):
            pass

# AI Integration - OpenAI ChatGPT
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("OpenAI package not installed. AI features will be limited. Run: pip install openai")

class AIAssistant:
    """AI Assistant class for ChatGPT integration."""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.available = OPENAI_AVAILABLE and self.api_key is not None
        
    def _get_api_key(self):
        """Get OpenAI API key from environment variables or Streamlit secrets."""
        if not OPENAI_AVAILABLE:
            return None
            
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                return st.secrets['OPENAI_API_KEY']
            # Try environment variable
            api_key = os.getenv('OPENAI_API_KEY')
            return api_key
        except:
            return None
    
    def get_ai_response(self, prompt, context="", max_tokens=500):
        """
        Get response from ChatGPT API.
        
        Args:
            prompt (str): The user's question
            context (str): Additional context for the AI
            max_tokens (int): Maximum response length
            
        Returns:
            str: AI response or error message
        """
        if not self.available:
            return "🤖 AI Assistant is not available. Please install OpenAI package and configure API key."
        
        if not self.api_key:
            return "🔑 OpenAI API key not configured. Please set OPENAI_API_KEY environment variable or add to Streamlit secrets."
        
        try:
            openai.api_key = self.api_key
            
            system_message = """
            You are an expert assistant for a Multi-Domain Intelligence Platform. 
            Provide helpful, professional responses about cybersecurity, data science, and IT operations.
            Be concise but thorough in your analysis and recommendations.
            """
            
            full_prompt = f"{context}\n\nUser Question: {prompt}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ AI Assistant Error: {str(e)}"

def check_authentication():
    """Check if user is logged in, redirect to login if not."""
    if not st.session_state.get('logged_in'):
        st.error("🔐 Please log in to access the dashboard")
        if st.button("Go to Login Page"):
            st.switch_page("pages/1_Login.py")
        st.stop()

def get_user_domain_access():
    """Determine which domains the current user can access based on role."""
    role = st.session_state.get('user_role', '').lower()
    
    domain_access = {
        'cybersecurity': False,
        'data_science': False,
        'it_operations': False
    }
    
    if 'cyber' in role or 'analyst' in role or role == 'admin':
        domain_access['cybersecurity'] = True
    if 'data' in role or 'scientist' in role or role == 'admin':
        domain_access['data_science'] = True
    if 'it' in role or 'admin' in role or 'operations' in role:
        domain_access['it_operations'] = True
        
    # If no specific role detected, grant all access
    if not any(domain_access.values()):
        domain_access = {domain: True for domain in domain_access}
    
    return domain_access

def create_cybersecurity_dashboard(db, ai_assistant):
    """Create Cybersecurity domain dashboard."""
    st.header("🔒 Cybersecurity Dashboard")
    st.markdown("---")
    
    # Get cyber incidents data - use get_all_records instead of get_cyber_incidents
    incidents = db.get_all_records("cyber_incidents")
    
    if not incidents:
        st.warning("No cyber incidents data available.")
        # Create sample data for demonstration
        sample_data = [
            (1, 'Phishing Attack', 'Suspicious email campaign', 'High', 'Open', 'Phishing', 'Analyst_1', 
             datetime.now() - timedelta(days=2), None, None),
            (2, 'Malware Detection', 'Ransomware detected on server', 'Critical', 'In Progress', 'Malware',
             'Analyst_2', datetime.now() - timedelta(days=1), None, None),
            (3, 'Unauthorized Access', 'Failed login attempts', 'Medium', 'Resolved', 'Access Control',
             'Analyst_1', datetime.now() - timedelta(days=5), datetime.now() - timedelta(days=4), 24.5),
            (4, 'Data Leak', 'Sensitive data exposure', 'High', 'Open', 'Data Breach',
             None, datetime.now() - timedelta(hours=12), None, None),
        ]
        df = pd.DataFrame(sample_data, columns=[
            'ID', 'Title', 'Description', 'Severity', 'Status', 'Category', 
            'Assigned_To', 'Date_Reported', 'Date_Resolved', 'Resolution_Time_Hours'
        ])
    else:
        # Convert to DataFrame
        df = pd.DataFrame(incidents, columns=[
            'ID', 'Title', 'Description', 'Severity', 'Status', 'Category', 
            'Assigned_To', 'Date_Reported', 'Date_Resolved', 'Resolution_Time_Hours'
        ])
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_incidents = len(df)
        st.metric("Total Incidents", total_incidents)
    
    with col2:
        open_incidents = len(df[df['Status'] == 'Open'])
        st.metric("Open Incidents", open_incidents)
    
    with col3:
        critical_incidents = len(df[df['Severity'] == 'Critical'])
        st.metric("Critical Incidents", critical_incidents)
    
    with col4:
        avg_resolution_time = df['Resolution_Time_Hours'].mean()
        st.metric("Avg Resolution (Hours)", f"{avg_resolution_time:.1f}" if not pd.isna(avg_resolution_time) else "N/A")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Severity distribution
        severity_counts = df['Severity'].value_counts()
        fig_severity = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Incidents by Severity",
            color=severity_counts.index,
            color_discrete_map={
                'Critical': 'red',
                'High': 'orange', 
                'Medium': 'yellow',
                'Low': 'green'
            }
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    with col2:
        # Status distribution
        status_counts = df['Status'].value_counts()
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Incidents by Status",
            color=status_counts.index,
            labels={'x': 'Status', 'y': 'Count'}
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # AI Assistant for Cybersecurity
    st.subheader("🦠 Cybersecurity AI Assistant")
    cybersecurity_context = f"""
    Current Cybersecurity Status:
    - Total incidents: {total_incidents}
    - Open incidents: {open_incidents} 
    - Critical incidents: {critical_incidents}
    - Average resolution time: {avg_resolution_time:.1f} hours
    
    Incident Distribution:
    {df['Category'].value_counts().to_string()}
    """
    
    cyber_question = st.text_input(
        "Ask about cybersecurity threats, incidents, or recommendations:",
        placeholder="e.g., How can we improve incident response times?",
        key="cyber_ai_input"
    )
    
    if st.button("Get AI Analysis", key="cyber_ai_btn"):
        if cyber_question:
            with st.spinner("Analyzing cybersecurity data..."):
                response = ai_assistant.get_ai_response(cyber_question, cybersecurity_context)
                st.markdown("### AI Analysis:")
                st.info(response)
        else:
            st.warning("Please enter a question for the AI assistant.")
    
    # Raw data table
    with st.expander("View Raw Incident Data"):
        st.dataframe(df)

def create_data_science_dashboard(db, ai_assistant):
    """Create Data Science domain dashboard."""
    st.header("📊 Data Science Dashboard")
    st.markdown("---")
    
    # Get datasets data - use get_all_records
    datasets = db.get_all_records("datasets_metadata")
    
    if not datasets:
        st.warning("No datasets metadata available.")
        # Create sample data for demonstration
        sample_data = [
            (1, 'Sales Data Q1', 'Quarterly sales figures', 'Sales', 125.5, 15000, 25, 0.85,
             datetime.now() - timedelta(days=30), datetime.now() - timedelta(days=2), 0),
            (2, 'Customer Feedback', 'Customer satisfaction survey results', 'Marketing', 45.2, 5000, 15, 0.92,
             datetime.now() - timedelta(days=15), datetime.now() - timedelta(days=1), 0),
            (3, 'Server Logs', 'Web server access logs', 'IT', 850.3, 250000, 8, 0.78,
             datetime.now() - timedelta(days=90), datetime.now() - timedelta(days=30), 1),
            (4, 'Financial Transactions', 'Bank transaction records', 'Finance', 320.7, 75000, 12, 0.95,
             datetime.now() - timedelta(days=7), datetime.now(), 0),
        ]
        df = pd.DataFrame(sample_data, columns=[
            'ID', 'Name', 'Description', 'Source_Department', 'File_Size_MB',
            'Row_Count', 'Column_Count', 'Data_Quality_Score', 'Upload_Date',
            'Last_Accessed', 'Is_Archived'
        ])
    else:
        # Convert to DataFrame
        df = pd.DataFrame(datasets, columns=[
            'ID', 'Name', 'Description', 'Source_Department', 'File_Size_MB',
            'Row_Count', 'Column_Count', 'Data_Quality_Score', 'Upload_Date',
            'Last_Accessed', 'Is_Archived'
        ])
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_datasets = len(df)
        st.metric("Total Datasets", total_datasets)
    
    with col2:
        total_size_gb = df['File_Size_MB'].sum() / 1024
        st.metric("Total Size (GB)", f"{total_size_gb:.1f}")
    
    with col3:
        avg_quality = df['Data_Quality_Score'].mean()
        st.metric("Avg Quality Score", f"{avg_quality:.2f}")
    
    with col4:
        archived_count = len(df[df['Is_Archived'] == 1])
        st.metric("Archived Datasets", archived_count)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Dataset size distribution
        fig_size = px.histogram(
            df, 
            x='File_Size_MB',
            title="Dataset Size Distribution (MB)",
            nbins=10
        )
        st.plotly_chart(fig_size, use_container_width=True)
    
    with col2:
        # Quality score distribution
        fig_quality = px.box(
            df,
            y='Data_Quality_Score',
            title="Data Quality Score Distribution"
        )
        st.plotly_chart(fig_quality, use_container_width=True)
    
    # Department analysis
    dept_counts = df['Source_Department'].value_counts()
    fig_dept = px.bar(
        x=dept_counts.index,
        y=dept_counts.values,
        title="Datasets by Source Department",
        labels={'x': 'Department', 'y': 'Count'}
    )
    st.plotly_chart(fig_dept, use_container_width=True)
    
    # AI Assistant for Data Science
    st.subheader("🔍 Data Science AI Assistant")
    datascience_context = f"""
    Current Data Science Status:
    - Total datasets: {total_datasets}
    - Total storage used: {total_size_gb:.1f} GB
    - Average data quality score: {avg_quality:.2f}
    - Archived datasets: {archived_count}
    
    Department Distribution:
    {dept_counts.to_string()}
    """
    
    ds_question = st.text_input(
        "Ask about data governance, quality, or management:",
        placeholder="e.g., Which departments need better data governance?",
        key="ds_ai_input"
    )
    
    if st.button("Get AI Analysis", key="ds_ai_btn"):
        if ds_question:
            with st.spinner("Analyzing data science metrics..."):
                response = ai_assistant.get_ai_response(ds_question, datascience_context)
                st.markdown("### AI Analysis:")
                st.info(response)
        else:
            st.warning("Please enter a question for the AI assistant.")
    
    # Dataset recommendations
    st.subheader("💡 Dataset Recommendations")
    
    # Find large, low-quality datasets
    large_low_quality = df[(df['File_Size_MB'] > 100) & (df['Data_Quality_Score'] < 0.7)]
    if not large_low_quality.empty:
        st.warning(f"**Action Needed:** {len(large_low_quality)} large datasets have low quality scores (< 0.7)")
        st.dataframe(large_low_quality[['Name', 'File_Size_MB', 'Data_Quality_Score']])

def create_it_operations_dashboard(db, ai_assistant):
    """Create IT Operations domain dashboard."""
    st.header("🖥️ IT Operations Dashboard")
    st.markdown("---")
    
    # Get IT tickets data - use get_all_records
    tickets = db.get_all_records("it_tickets")
    
    if not tickets:
        st.warning("No IT tickets data available.")
        # Create sample data for demonstration
        sample_data = [
            (1, 'Printer not working', 'Printer in room 401 is offline', 'IT_Support_1', 'User_123', 'New',
             'Medium', 'Hardware', datetime.now() - timedelta(hours=3), None, None, None),
            (2, 'Email access issue', 'Cannot access email on mobile', 'IT_Support_2', 'User_456', 'In Progress',
             'High', 'Software', datetime.now() - timedelta(days=1), datetime.now() - timedelta(hours=12), None, None),
            (3, 'VPN connection problem', 'VPN disconnects frequently', 'IT_Support_1', 'User_789', 'Resolved',
             'Urgent', 'Network', datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1), 
             datetime.now() - timedelta(hours=6), 'Updated VPN client software'),
            (4, 'Software license renewal', 'Adobe Creative Cloud license expiring', None, 'Admin_1', 'New',
             'Low', 'License', datetime.now() - timedelta(hours=1), None, None, None),
        ]
        df = pd.DataFrame(sample_data, columns=[
            'ID', 'Title', 'Description', 'Assignee', 'Reporter', 'Status',
            'Priority', 'Category', 'Date_Created', 'Date_Assigned', 
            'Date_Resolved', 'Resolution_Notes'
        ])
    else:
        # Convert to DataFrame
        df = pd.DataFrame(tickets, columns=[
            'ID', 'Title', 'Description', 'Assignee', 'Reporter', 'Status',
            'Priority', 'Category', 'Date_Created', 'Date_Assigned', 
            'Date_Resolved', 'Resolution_Notes'
        ])
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tickets = len(df)
        st.metric("Total Tickets", total_tickets)
    
    with col2:
        open_tickets = len(df[df['Status'].isin(['New', 'Assigned', 'In Progress'])])
        st.metric("Open Tickets", open_tickets)
    
    with col3:
        urgent_tickets = len(df[df['Priority'] == 'Urgent'])
        st.metric("Urgent Tickets", urgent_tickets)
    
    with col4:
        waiting_tickets = len(df[df['Status'] == 'Waiting for User'])
        st.metric("Waiting for User", waiting_tickets)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Priority distribution
        priority_counts = df['Priority'].value_counts()
        fig_priority = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Tickets by Priority",
            color=priority_counts.index,
            color_discrete_map={
                'Urgent': 'red',
                'High': 'orange',
                'Medium': 'yellow',
                'Low': 'green'
            }
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Status distribution
        status_counts = df['Status'].value_counts()
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Tickets by Status",
            color=status_counts.index
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Performance analysis
    st.subheader("📈 Performance Analysis")
    
    # Assignee performance (simulated resolution times)
    if 'Assignee' in df.columns and not df['Assignee'].isna().all():
        assignee_performance = df['Assignee'].value_counts().head(5)
        fig_assignee = px.bar(
            x=assignee_performance.index,
            y=assignee_performance.values,
            title="Top 5 Assignees by Ticket Count"
        )
        st.plotly_chart(fig_assignee, use_container_width=True)
    
    # AI Assistant for IT Operations
    st.subheader("🔧 IT Operations AI Assistant")
    it_context = f"""
    Current IT Operations Status:
    - Total tickets: {total_tickets}
    - Open tickets: {open_tickets}
    - Urgent tickets: {urgent_tickets}
    - Tickets waiting for user: {waiting_tickets}
    
    Priority Distribution:
    {priority_counts.to_string()}
    
    Status Distribution:
    {status_counts.to_string()}
    """
    
    it_question = st.text_input(
        "Ask about IT performance, bottlenecks, or improvements:",
        placeholder="e.g., How can we reduce ticket resolution times?",
        key="it_ai_input"
    )
    
    if st.button("Get AI Analysis", key="it_ai_btn"):
        if it_question:
            with st.spinner("Analyzing IT operations data..."):
                response = ai_assistant.get_ai_response(it_question, it_context)
                st.markdown("### AI Analysis:")
                st.info(response)
        else:
            st.warning("Please enter a question for the AI assistant.")
    
    # Bottleneck identification
    st.subheader("🚨 Potential Bottlenecks")
    
    if waiting_tickets > total_tickets * 0.3:  # More than 30% waiting for user
        st.error(f"**Bottleneck Alert:** {waiting_tickets} tickets ({waiting_tickets/total_tickets*100:.1f}%) are waiting for user response")
        st.info("**Recommendation:** Implement automated follow-up reminders for users")
    
    if urgent_tickets > 5:
        st.warning(f"**High Priority Alert:** {urgent_tickets} urgent tickets need immediate attention")

def main():
    """Main dashboard function."""
    # Check authentication
    check_authentication()
    
    # Set page configuration
    st.set_page_config(
        page_title="Dashboard - Intelligence Platform",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize AI Assistant
    ai_assistant = AIAssistant()
    
    # Database connection
    db = DatabaseManager()
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("🏢 Multi-Domain Intelligence Platform")
        st.markdown(f"Welcome back, **{st.session_state.get('username', 'User')}**! | Role: **{st.session_state.get('user_role', 'User')}**")
    
    with col2:
        st.metric("Session Active", "✅ Online")
    
    with col3:
        if st.button("🚪 Logout"):
            # Clear session state
            for key in ['logged_in', 'username', 'user_role', 'user_id']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
            st.switch_page("pages/1_Login.py")
    
    st.markdown("---")
    
    # Get user's domain access
    domain_access = get_user_domain_access()
    
    # Domain navigation
    st.sidebar.header("🔍 Navigation")
    
    # Domain selection
    available_domains = []
    if domain_access['cybersecurity']:
        available_domains.append("🔒 Cybersecurity")
    if domain_access['data_science']:
        available_domains.append("📊 Data Science")
    if domain_access['it_operations']:
        available_domains.append("🖥️ IT Operations")
    
    if available_domains:
        selected_domain = st.sidebar.radio(
            "Select Domain:",
            available_domains,
            index=0
        )
    else:
        st.sidebar.warning("No domains available for your role")
        selected_domain = None
    
    # Quick metrics in sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("📈 Quick Stats")
    
    try:
        # Get quick stats for each domain using get_all_records
        cyber_incidents = db.get_all_records("cyber_incidents")
        datasets = db.get_all_records("datasets_metadata")
        it_tickets = db.get_all_records("it_tickets")
        
        if domain_access['cybersecurity'] and cyber_incidents:
            # Convert to DataFrame to access status
            if cyber_incidents:
                df_cyber = pd.DataFrame(cyber_incidents, columns=['ID', 'Title', 'Description', 'Severity', 'Status', 'Category', 
                    'Assigned_To', 'Date_Reported', 'Date_Resolved', 'Resolution_Time_Hours'])
                open_cyber = len(df_cyber[df_cyber['Status'] == 'Open'])
                st.sidebar.metric("Open Security Incidents", open_cyber)
        
        if domain_access['data_science'] and datasets:
            if datasets:
                df_data = pd.DataFrame(datasets, columns=['ID', 'Name', 'Description', 'Source_Department', 'File_Size_MB',
                    'Row_Count', 'Column_Count', 'Data_Quality_Score', 'Upload_Date', 'Last_Accessed', 'Is_Archived'])
                total_size = df_data['File_Size_MB'].sum() / 1024
                st.sidebar.metric("Total Data (GB)", f"{total_size:.1f}")
        
        if domain_access['it_operations'] and it_tickets:
            if it_tickets:
                df_it = pd.DataFrame(it_tickets, columns=['ID', 'Title', 'Description', 'Assignee', 'Reporter', 'Status',
                    'Priority', 'Category', 'Date_Created', 'Date_Assigned', 'Date_Resolved', 'Resolution_Notes'])
                open_tickets = len(df_it[df_it['Status'].isin(['New', 'Assigned', 'In Progress'])])
                st.sidebar.metric("Open IT Tickets", open_tickets)
            
    except Exception as e:
        st.sidebar.warning("Could not load quick stats. Data may not be available yet.")
    
    # AI Assistant in sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 AI Assistant")
    
    sidebar_question = st.sidebar.text_area(
        "Ask me anything about your data:",
        placeholder="e.g., What are the main insights from our data?",
        height=100
    )
    
    if st.sidebar.button("Ask AI", use_container_width=True):
        if sidebar_question:
            with st.spinner("Consulting AI assistant..."):
                response = ai_assistant.get_ai_response(sidebar_question)
                st.sidebar.markdown("### AI Response:")
                st.sidebar.info(response)
        else:
            st.sidebar.warning("Please enter a question")
    
    # Display selected domain dashboard
    if selected_domain:
        if "Cybersecurity" in selected_domain and domain_access['cybersecurity']:
            create_cybersecurity_dashboard(db, ai_assistant)
        elif "Data Science" in selected_domain and domain_access['data_science']:
            create_data_science_dashboard(db, ai_assistant)
        elif "IT Operations" in selected_domain and domain_access['it_operations']:
            create_it_operations_dashboard(db, ai_assistant)
    else:
        st.info("Please select a domain from the sidebar to view dashboard.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        Multi-Domain Intelligence Platform | Built with Streamlit & Python | AI-Powered Analytics
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()