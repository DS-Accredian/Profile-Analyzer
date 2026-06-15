import streamlit as st

def render_step2():
    st.subheader("Step 2: Define Your Strategy")
    st.write("We need to understand your exact positioning to engineer the perfect AI data-extraction prompt.")
    
    # Keep the text input for specific role context
    industry = st.text_input("First, what is your specific Target Role & Industry?", placeholder="e.g., Senior Product Manager in FinTech")
    
    st.write("---")
    
    objective = st.radio(
        "1. What is your immediate primary objective on LinkedIn?",
        options=[
            "Landing a new full-time role (Active/Passive Job Search)",
            "Attracting freelance clients & B2B leads (Social Selling)",
            "Building thought leadership & audience (Personal Branding)",
            "Positioning for Board Seats & Executive level (C-Suite/NED)"
        ]
    )
    
    audience = st.radio(
        "2. Who is the #1 decision-maker you need to impress?",
        options=[
            "Recruiters & Talent Acquisition",
            "Founders, VCs & Investors",
            "Target Clients & B2B Buyers",
            "Conference Organizers & Media"
        ]
    )
    
    weakness = st.radio(
        "3. What feels like the weakest link in your current profile?",
        options=[
            "Invisible: Weak SEO, missing keywords, and low search appearances",
            "Boring: Reads like a dry resume, lacks a compelling human story",
            "Unproven: Missing quantified metrics, recommendations, and portfolio",
            "Quiet: No content strategy, weak network outreach, low engagement"
        ]
    )
    
    seniority = st.radio(
        "4. What is your current career stage?",
        options=[
            "Student / Early Career (0-3 years)",
            "Mid-Level Professional (4-9 years)",
            "Senior Leadership (Director/VP/Head of)",
            "Founder / C-Suite / Board Member"
        ]
    )
    
    st.write("---")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Back"):
            st.session_state["step"] = 1
            st.rerun()
    with col2:
        if st.button("Generate AI Prompt"):
            if industry.strip() == "":
                st.warning("Please enter your target industry/role at the top.")
            else:
                # Save all the new data points to session state
                st.session_state["industry"] = industry
                st.session_state["objective"] = objective
                st.session_state["audience"] = audience
                st.session_state["weakness"] = weakness
                st.session_state["seniority"] = seniority
                
                st.session_state["step"] = 3
                st.rerun()