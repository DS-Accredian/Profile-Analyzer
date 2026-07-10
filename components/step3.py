# import streamlit as st
# from utils.prompt_builder import build_prompt

# def render_step3():
#     st.subheader("Step 3: Generate Your AI Audit")
#     st.write("1. Copy the engineered prompt below.")
#     st.write("2. Open your preferred AI. (Claude 3.5 Sonnet or ChatGPT-4o recommended)")
#     st.write("3. Paste the prompt, wait for the generation, and copy the resulting report.")
    
#     # Build prompt from session state variables

#     prompt_text = build_prompt(
#         url=st.session_state.get("linkedin_url", ""),
#         industry=st.session_state.get("industry", ""),
#         objective=st.session_state.get("objective", ""),
#         audience=st.session_state.get("audience", ""),
#         weakness=st.session_state.get("weakness", ""),
#         seniority=st.session_state.get("seniority", "")
#     )
    
#     # st.code natively has a copy button in the top right corner
#     st.code(prompt_text, language="markdown")
    
#     st.write("---")
#     st.write("**Run this prompt in one of the following:**")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.link_button("Go to Claude", "https://claude.ai")
#     with col2:
#         st.link_button("Go to ChatGPT", "https://chatgpt.com")
#     with col3:
#         st.link_button("Go to Groq", "https://groq.com")
        
#     st.write("---")
    
#     col_back, col_next = st.columns([1, 4])
#     with col_back:
#         if st.button("Back"):
#             st.session_state["step"] = 2
#             st.rerun()
#     with col_next:
#         if st.button("Next: Import AI Audit Report"):
#             st.session_state["step"] = 4
#             st.rerun()

import streamlit as st
from utils.prompt_builder import build_prompt
from st_copy_to_clipboard import st_copy_to_clipboard

def render_step3():
    st.subheader("Step 3: Generate Your AI Audit")
    
    # 1. Clear Instructions
    st.write("We have engineered a highly-advanced prompt based on your exact career stage and weaknesses.")
    st.write("1. Click the **Copy Prompt** button below.")
    st.write("2. Open your preferred AI (Claude 3.5 Sonnet, ChatGPT-4o, etc.).")
    st.write("3. Paste the prompt, wait for the generation, and copy the resulting report.")
    
    # 2. Build the prompt from session state variables
    prompt_text = build_prompt(
        url=st.session_state.get("linkedin_url", ""),
        industry=st.session_state.get("industry", ""),
        objective=st.session_state.get("objective", ""),
        audience=st.session_state.get("audience", ""),
        weakness=st.session_state.get("weakness", ""),
        seniority=st.session_state.get("seniority", "")
    )
    
    st.write("---")
    
    # 3. The Standalone Copy Button (Always Visible)
    st.write("### ✂️ Your Engineered Prompt")
    st_copy_to_clipboard(
        text=prompt_text,
        before_copy_label="📋 Copy Full Prompt to Clipboard",
        after_copy_label="✅ Copied Successfully!"
    )
    
    # 4. The Collapsed Expander (For the curious users)
    with st.expander("👀 Want to read the prompt before copying? Click to expand."):
        st.info("You don't need to read this to use it, but here is the exact code we generated for you:")
        st.code(prompt_text, language="markdown")
    
    st.write("---")
    
    # 5. External AI Links
    st.write("**Run this prompt in one of the following:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("Go to Claude", "https://claude.ai", use_container_width=True)
    with col2:
        st.link_button("Go to ChatGPT", "https://chatgpt.com", use_container_width=True)
    with col3:
        st.link_button("Go to Gemini", "https://gemini.com", use_container_width=True)
        
    st.write("---")
    
    # 6. Navigation
    col_back, col_next = st.columns([1, 4])
    with col_back:
        if st.button("Back"):
            st.session_state["step"] = 2
            st.rerun()
    with col_next:
        if st.button("Next: Import AI Audit Report"):
            st.session_state["step"] = 4
            st.rerun()
