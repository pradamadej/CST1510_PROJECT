# pages/dashboard.py - FIXED VERSION
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Try to import bcrypt with fallback
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    st.warning("Note: bcrypt not installed. Password features limited.")

def main():
    """Main dashboard function"""
    
    # Set page title
    st.title("📊 Intelligence Dashboard")
    
    # Get username from session state
    username = st.session_state.get('username', 'User')
    st.success(f"Welcome back, {username}!")
    
    # Display bcrypt status
    if not BCRYPT_AVAILABLE:
        st.info("🔐 For password hashing features, install bcrypt in requirements.txt")
    
    # Dashboard overview
    st.markdown("### 📈 Platform Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users", "24", "+3")
    with col2:
        st.metric("Security Score", "94%", "+2%")
    with col2:
        st.metric("Data Quality", "88%", "+5%")
    with col4:
        st.metric("System Health", "99%", "-1%")
    
    st.markdown("---")
    
    # Create tabs for different domains
    tab1, tab2, tab3 = st.tabs(["Security", "Data Analytics", "Operations"])
    
    with tab1:
        show_security_tab()
    
    with tab2:
        show_data_analytics_tab()
    
    with tab3:
        show_operations_tab()
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def show_security_tab():
    """Security dashboard tab"""
    st.header("🔒 Security Dashboard")
    
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
    
    security_data = pd.DataFrame({
        "Time": ["10:30", "11:15", "12:45", "14:20"],
        "Event": ["Failed login attempt", "Port scan detected", "Firewall updated", "Virus scan clean"],
        "Severity": ["Medium", "High", "Low", "Low"],
        "Status": ["Resolved", "Investigating", "Completed", "Clean"]
    })
    
    st.dataframe(security_data, use_container_width=True)
    
    # Quick security actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Run Security Scan", key="scan_btn"):
            st.info("Security scan initiated...")
    
    with col2:
        if st.button("View All Incidents", key="incidents_btn"):
            st.info("Loading incident log...")

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
        "Dataset": ["Customer Data", "Sales Data", "Inventory", "Logs"],
        "Completeness": [92, 85, 96, 78],
        "Accuracy": [88, 91, 94, 82],
        "Timeliness": [95, 87, 90, 76]
    })
    
    st.dataframe(quality_data, use_container_width=True)

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
        {"Service": "Web Server", "Status": "✅ Running", "Uptime": "99.9%"},
        {"Service": "Database", "Status": "✅ Running", "Uptime": "99.8%"},
        {"Service": "API Gateway", "Status": "⚠️ Slow", "Uptime": "98.5%"},
        {"Service": "Cache", "Status": "✅ Running", "Uptime": "99.7%"},
        {"Service": "Monitoring", "Status": "✅ Running", "Uptime": "100%"},
    ]
    
    for service in services:
        cols = st.columns([2, 1, 1])
        with cols[0]:
            st.write(f"**{service['Service']}**")
        with cols[1]:
            st.write(service['Status'])
        with cols[2]:
            st.write(service['Uptime'])
    
    # Recent system alerts
    st.subheader("Recent Alerts")
    
    alerts = [
        {"Time": "09:30", "Alert": "High CPU Usage", "Severity": "Warning"},
        {"Time": "11:15", "Alert": "Memory Pressure", "Severity": "Critical"},
        {"Time": "13:45", "Alert": "Network Latency", "Severity": "Warning"},
    ]
    
    for alert in alerts:
        severity_color = "🔴" if alert["Severity"] == "Critical" else "🟡"
        st.write(f"**{alert['Time']}** {severity_color} {alert['Alert']}")

if __name__ == "__main__":
    main()