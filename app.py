"""
Simple redirect app to handle page navigation
"""

import streamlit as st

# Set page config first
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🏢",
    layout="wide"
)

# Simple redirect logic
st.title("Multi-Domain Intelligence Platform")
st.markdown("## Loading...")

# Check if logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Redirect to dashboard
    try:
        # Use JavaScript redirect as fallback
        js = f"""
        <script>
            window.location.href = "/Dashboard";
        </script>
        """
        st.components.v1.html(js, height=0)
    except:
        st.info("You are logged in. Please visit the Dashboard page.")
        if st.button("Go to Dashboard"):
            st.switch_page("pages/2_Dashboard.py")
else:
    # Redirect to login
    try:
        # Use JavaScript redirect as fallback
        js = f"""
        <script>
            window.location.href = "/Login";
        </script>
        """
        st.components.v1.html(js, height=0)
    except:
        st.info("Please log in to access the platform.")
        if st.button("Go to Login"):
            st.switch_page("pages/1_Login.py")