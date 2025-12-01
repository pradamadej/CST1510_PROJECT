# pages/dashboard.py
import streamlit as st

def main():
    """Main dashboard function - NO set_page_config here!"""
    
    # Title
    st.title("📊 Intelligence Dashboard")
    
    # Welcome message
    st.success(f"Welcome, {st.session_state.get('username', 'User')}!")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Security", "Analytics", "Operations"])
    
    with tab1:
        st.header("🔒 Security Dashboard")
        
        # Security metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Threats", "12", "+2")
        with col2:
            st.metric("Incidents", "3", "0")
        with col3:
            st.metric("Prevented", "89", "+15")
        
        # Security log
        st.subheader("Recent Security Events")
        security_data = [
            {"Time": "10:30", "Event": "Failed login attempt", "Severity": "Medium", "Status": "Resolved"},
            {"Time": "11:15", "Event": "Port scan detected", "Severity": "High", "Status": "Investigating"},
            {"Time": "12:45", "Event": "Firewall rule updated", "Severity": "Low", "Status": "Completed"},
            {"Time": "14:20", "Event": "Malware scan completed", "Severity": "Low", "Status": "Clean"},
        ]
        st.table(security_data)
    
    with tab2:
        st.header("📈 Analytics Dashboard")
        
        # Data metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Volume", "2.4 TB", "+0.3 TB")
        with col2:
            st.metric("Processing Jobs", "156", "+24")
        with col3:
            st.metric("Accuracy", "94.2%", "+1.8%")
        
        # Sample data
        st.subheader("Performance Metrics")
        import pandas as pd
        import numpy as np
        
        # Generate sample data
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        data = pd.DataFrame({
            'Date': dates,
            'Throughput': np.random.randint(100, 1000, 30),
            'Latency': np.random.randint(10, 100, 30),
            'Errors': np.random.randint(0, 10, 30)
        })
        
        st.line_chart(data.set_index('Date')[['Throughput', 'Latency']])
        
        st.subheader("Data Summary")
        st.dataframe(data.describe())
    
    with tab3:
        st.header("🖥️ Operations Dashboard")
        
        # System metrics
        st.subheader("System Health")
        
        col1, col2 = st.columns(2)
        with col1:
            st.progress(0.75, text="CPU Usage: 75%")
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
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{service['Service']}**")
            with col2:
                st.write(service['Status'])
            with col3:
                st.write(service['Uptime'])
    
    # Footer
    st.markdown("---")
    st.caption("Last updated: Just now | Auto-refresh every 5 minutes")

if __name__ == "__main__":
    main()