import streamlit as st

def render_step1():
    st.subheader("Step 1: Connect Your Profile")
    st.write("Welcome to LinkedBoost! Let's start by analyzing your current LinkedIn presence.")
    
    url = st.text_input("Enter your LinkedIn Profile URL:", placeholder="https://www.linkedin.com/in/yourname")
    
    if st.button("Next"):
        if "linkedin.com/in/" in url or "linkedin.com/pub/" in url:
            st.session_state["linkedin_url"] = url
            st.session_state["step"] = 2
            st.rerun()
        else:
            st.error("Please enter a valid LinkedIn URL (must contain 'linkedin.com/in/' or 'linkedin.com/pub/').")
