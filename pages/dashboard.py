# pages/dashboard.py - SECURE VERSION
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def main():
    """Main dashboard function - REQUIRES LOGIN"""
    
    # CRITICAL: Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.error("🔒 Access Denied")
        st.warning("You must be logged in to access the dashboard.")
        st.info("Please go to the main page and log in.")
        
        # Add a login button
        if st.button("Go to Login Page"):
            # Clear any existing page config issues
            st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)
        
        # Stop execution here - don't show any dashboard content
        st.stop()
    
    # Only show dashboard if user is logged in
    username = st.session_state.get('username', 'User')
    
    # Set page title
    st.title("📊 Intelligence Dashboard")
    st.success(f"Welcome, {username}! 👋")
    
    # Dashboard overview
    st.markdown("### 📈 Platform Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users", "24", "+3")
    with col2:
        st.metric("Security Score", "94%", "+2%")
    with col3:
        st.metric("Data Quality", "88%", "+5%")
    with col4:
        st.metric("System Health", "99%", "-1%")
    
    st.markdown("---")
    
    # Create tabs for different domains
    tab1, tab2, tab3, tab4 = st.tabs(["Security", "Data", "Operations", "User Info"])
    
    with tab1:
        show_security_tab(username)
    
    with tab2:
        show_data_analytics_tab()
    
    with tab3:
        show_operations_tab()
    
    with tab4:
        show_user_info_tab(username)
    
    # Logout button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Logged out successfully!")
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.caption(f"Session: {username} | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def show_security_tab(username):
    """Security dashboard tab"""
    st.header("🔒 Security Dashboard")
    
    # User-specific welcome
    st.info(f"Security overview for **{username}**")
    
    # Security metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Threats Blocked", "128", "+12")
    with col2:
        st.metric("Active Incidents", "5", "-2")
    with col3:
        st.metric("Compliance", "92%", "+3%")
    
    # Recent security events
    st.subheader("Recent Security Events")
    
    # Generate user-specific data
    security_data = pd.DataFrame({
        "Time": ["10:30", "11:15", "12:45", "14:20", "15:30"],
        "Event": [
            f"Login: {username}",
            "Port scan detected",
            "Firewall rule updated",
            "Malware scan completed",
            f"Access review: {username}"
        ],
        "Severity": ["Info", "High", "Low", "Low", "Medium"],
        "Status": ["Success", "Investigating", "Completed", "Clean", "Review"]
    })
    
    st.dataframe(security_data, use_container_width=True, hide_index=True)
    
    # User-specific security actions
    st.subheader("Your Security Actions")
    
    if st.button(f"🔒 Run Security Check for {username}", key="user_security_check"):
        st.success(f"Security check initiated for {username}...")
        st.info("Checking login history, access patterns, and security compliance...")
    
    if st.button("📋 View My Access Log", key="user_access_log"):
        st.info(f"Loading access log for {username}...")
        
        # Simulated access log
        access_log = pd.DataFrame({
            "Timestamp": [
                datetime.now().strftime("%H:%M"),
                (datetime.now() - pd.Timedelta(hours=1)).strftime("%H:%M"),
                (datetime.now() - pd.Timedelta(hours=3)).strftime("%H:%M"),
                (datetime.now() - pd.Timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
            ],
            "Action": ["Dashboard Access", "Data Query", "Report Generation", "Login"],
            "IP Address": ["192.168.1.100", "192.168.1.100", "192.168.1.100", "192.168.1.100"],
            "Status": ["Success", "Success", "Success", "Success"]
        })
        
        st.dataframe(access_log, use_container_width=True)

def show_data_analytics_tab():
    """Data analytics dashboard tab"""
    st.header("📊 Data Analytics Dashboard")
    
    # Data metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Data Processed", "2.4 TB", "+0.3 TB")
    with col2:
        st.metric("Active Jobs", "12", "+2")
    with col3:
        st.metric("Accuracy Rate", "96.2%", "+1.8%")
    
    # Sample data chart
    st.subheader("Data Processing Trend")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Processed (GB)': np.random.randint(100, 1000, 30),
        'Errors': np.random.randint(0, 10, 30),
        'Success Rate (%)': np.random.randint(85, 100, 30)
    })
    
    st.line_chart(data.set_index('Date')[['Processed (GB)', 'Errors']])
    
    # Data quality
    st.subheader("Data Quality Metrics")
    
    quality_data = pd.DataFrame({
        "Dataset": ["Customer Data", "Sales Data", "Inventory", "Logs", "User Data"],
        "Completeness": [92, 85, 96, 78, 95],
        "Accuracy": [88, 91, 94, 82, 90],
        "Timeliness": [95, 87, 90, 76, 98]
    })
    
    st.dataframe(quality_data, use_container_width=True, hide_index=True)

def show_operations_tab():
    """Operations dashboard tab"""
    st.header("🖥️ IT Operations Dashboard")
    
    # System health indicators
    st.subheader("System Health")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.progress(0.75, text="CPU: 75%")
        st.progress(0.88, text="Memory: 88%")
    
    with col2:
        st.progress(0.45, text="Disk: 45%")
        st.progress(0.95, text="Network: 95%")
    
    # Service status
    st.subheader("Service Status")
    
    services = [
        {"Service": "Authentication", "Status": "✅ Running", "Uptime": "99.9%", "Users": "24"},
        {"Service": "Database", "Status": "✅ Running", "Uptime": "99.8%", "Queries": "1.2k"},
        {"Service": "API Gateway", "Status": "⚠️ Slow", "Uptime": "98.5%", "Requests": "5.4k"},
        {"Service": "Cache", "Status": "✅ Running", "Uptime": "99.7%", "Hit Rate": "94%"},
        {"Service": "Monitoring", "Status": "✅ Running", "Uptime": "100%", "Alerts": "12"},
    ]
    
    for service in services:
        cols = st.columns([2, 1, 1, 1])
        with cols[0]:
            st.write(f"**{service['Service']}**")
        with cols[1]:
            st.write(service['Status'])
        with cols[2]:
            st.write(service['Uptime'])
        with cols[3]:
            st.write(service['Users'] if 'Users' in service else service.get('Queries', service.get('Requests', service.get('Hit Rate', service.get('Alerts', '')))))
    
    # Quick actions
    st.subheader("System Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Services", use_container_width=True):
            st.success("Service refresh initiated...")
    
    with col2:
        if st.button("📊 View System Logs", use_container_width=True):
            st.info("Loading system logs...")

def show_user_info_tab(username):
    """User information tab"""
    st.header("👤 User Information")
    
    # User profile
    st.subheader("Your Profile")
    
    # Display user info from session state
    user_role = st.session_state.get('user_role', 'Analyst')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Username", username)
        st.metric("Role", user_role)
    
    with col2:
        # User activity stats
        st.metric("Session Duration", "45m")
        st.metric("Actions Today", "28")
    
    # User permissions
    st.subheader("Your Permissions")
    
    # Define permissions based on role
    permissions = {
        'admin': ['Full Access', 'User Management', 'System Configuration', 'Data Management', 'Security Controls'],
        'analyst': ['Data View', 'Report Generation', 'Basic Analytics', 'Dashboard Access'],
        'scientist': ['Data Analysis', 'Model Training', 'Advanced Analytics', 'Experiment Management'],
        'viewer': ['Read-only Access', 'Dashboard View', 'Basic Reports']
    }
    
    user_permissions = permissions.get(user_role.lower(), permissions['viewer'])
    
    for perm in user_permissions:
        st.write(f"✅ {perm}")
    
    # Account actions
    st.subheader("Account Actions")
    
    if st.button("🔄 Change Password", key="change_pass"):
        st.info("Password change functionality would be implemented here.")
    
    if st.button("📊 View Activity History", key="view_history"):
        st.info(f"Loading activity history for {username}...")
        
        # Simulated activity history
        history = pd.DataFrame({
            "Date": ["2024-01-15", "2024-01-14", "2024-01-13", "2024-01-12"],
            "Activity": ["Dashboard Access", "Report Generated", "Data Export", "Login"],
            "Duration": ["45m", "1h 20m", "30m", "2h 15m"],
            "Status": ["Completed", "Completed", "Completed", "Completed"]
        })
        
        st.dataframe(history, use_container_width=True, hide_index=True)

# Security check at module level
if __name__ == "__main__":
    # This allows direct execution for testing
    # In Streamlit Cloud, the main() function will be called directly
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = "Test User"
    
    main()