"""
Main Application File for Multi-Domain Intelligence Platform
File: app.py
"""

import streamlit as st

def main():
    """
    Main application entry point.
    Streamlit automatically detects pages in the 'pages' folder.
    """
    st.set_page_config(
        page_title="Multi-Domain Intelligence Platform",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Welcome page when accessing the main app
    st.title("🏢 Multi-Domain Intelligence Platform")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to Your Unified Intelligence Platform
        
        This platform provides comprehensive analytics and operational capabilities 
        for three key domains:
        
        - **🔒 Cybersecurity**: Incident response and threat analysis
        - **📊 Data Science**: Dataset governance and quality management  
        - **🖥️ IT Operations**: Service desk performance and ticket management
        
        ### Getting Started:
        1. **Navigate to the Login page** using the sidebar
        2. **Use demo credentials** for testing (see login page)
        3. **Explore dashboards** based on your role
        4. **Analyze data** and generate insights
        
        ### Security Features:
        - Secure password hashing with bcrypt
        - Role-based access control
        - Session management
        - SQL injection prevention
        """)
    
    with col2:
        st.info("""
        **Quick Access**
        
        Use the sidebar to navigate to:
        - 🔐 Login page
        - 📊 Dashboard (after login)
        - Domain-specific analytics
        
        **Need Help?**
        Check the login page for demo accounts and role information.
        """)
        
        if st.button("🚀 Go to Login Page"):
            st.switch_page("pages/1_Login.py")

if __name__ == "__main__":
    main()