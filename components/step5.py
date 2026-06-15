import streamlit as st
import json
import os
from utils.pdf_generator import generate_blueprint_pdf

def load_prompt_library():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "utils", "prompt_library.json")
    
    if not os.path.exists(file_path):
        file_path = os.path.join("utils", "prompt_library.json")
        
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []

def render_step5():
    st.subheader("Step 5: Your AI-Curated Blueprint")
    
    groq_data = st.session_state.get("groq_analysis", {})
    
    health_score = groq_data.get("parsed_health_score", "N/A")
    executive_summary = groq_data.get("executive_summary", "No summary provided.")
    top_gaps = groq_data.get("top_gaps_explained", ["No gaps identified."])
    raw_recommended_ids = groq_data.get("recommended_prompt_ids", [])
    
    # 1. Display Groq's Smart Metrics
    st.info(f"**Profile Health Score:** {health_score}/100")
    st.write(f"**Executive Summary:** {executive_summary}")
    
    st.warning("**Top Critical Gaps:**")
    for gap in top_gaps:
        st.markdown(f"- {gap}")
    
    st.write("---")
    st.write("### Tactical Rewrite Library")
    st.write("Based on Groq's semantic analysis, here are the exact prompts to fix your profile.")
    
    # 2. BULLETPROOF ID MATCHING
    all_prompts = load_prompt_library()
    
    safe_recommended_ids = [str(r_id) for r_id in raw_recommended_ids]
    
    recommended_prompts = [
        p for p in all_prompts 
        if str(p.get("id")) in safe_recommended_ids
    ]
    
    if not recommended_prompts and all_prompts:
        recommended_prompts = all_prompts[:min(3, len(all_prompts))]
        st.caption("*(Note: Default foundational prompts loaded)*")
    
    # 3. Render Prompts
    if recommended_prompts:
        for i, prompt_data in enumerate(recommended_prompts):
            with st.expander(f"{prompt_data.get('title', 'Prompt')} (Section: {prompt_data.get('section', 'General')})", expanded=(i==0)):
                st.write(f"**Why use this:** {prompt_data.get('description', '')}")
                st.code(prompt_data.get("prompt", ""), language="markdown")
                if prompt_data.get("pro_tips"):
                    st.caption("**Pro Tips:**")
                    for tip in prompt_data["pro_tips"]:
                        st.caption(f"- {tip}")
    else:
        st.error("Prompt library is completely empty. Please check your prompt_library.json file.")

    st.write("---")

    # 4. THE OPTIMIZATION LOOP INSTRUCTIONS
    st.subheader("🔁 The Optimization Loop")
    st.success(
        """
        **What to do next:**
        1. **Execute:** Copy the prompts above and run them in your preferred AI (ChatGPT, Claude, etc.).
        2. **Apply:** Take the AI's optimized rewrites and update your actual LinkedIn profile.
        3. **Re-Test:** Once your profile is updated, come back here, click **Start Over**, and run a fresh audit to watch your Profile Health Score climb!
        """
    )
    
    st.write("---")
    
    # 5. PDF & Reset Buttons
    col1, col2 = st.columns(2)
    with col1:
        # Safely convert top_gaps list into a string for the PDF
        if isinstance(top_gaps, list):
            gaps_string = "\n".join([f"- {g}" for g in top_gaps])
        else:
            gaps_string = str(top_gaps)
            
        try:
            pdf_bytes = generate_blueprint_pdf(health_score, gaps_string, recommended_prompts)
            st.download_button(
                label="📄 Download PDF Blueprint",
                data=pdf_bytes,
                file_name="LinkedBoost_Blueprint.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF Generation Error: {e}")
            
    with col2:
        if st.button("Start Over (Clear Data)", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()