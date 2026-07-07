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
    strategic_gaps = groq_data.get("strategic_gaps", [])
    
    # 1. Display Groq's Smart Metrics
    st.info(f"**Profile Health Score:** {health_score}/100")
    st.write(f"**Executive Summary:** {executive_summary}")
    
    st.write("---")
    st.write("### Tactical Rewrite Library")
    st.write("Based on Groq's semantic analysis, we have identified your core gaps. For each gap, choose **Option A** or **Option B** based on the style that fits you best.")
    
    # 2. BULLETPROOF ID MATCHING & UI RENDERING
    all_prompts = load_prompt_library()
    prompt_dict = {str(p.get("id")): p for p in all_prompts} # Quick lookup dictionary
    
    flat_pdf_prompts = [] # We will collect the chosen prompts here for the PDF
    gaps_for_pdf = [] # Collect strings for the PDF
    
    if strategic_gaps:
        for index, gap in enumerate(strategic_gaps, 1):
            gap_name = gap.get("gap_name", "Profile Gap")
            explanation = gap.get("explanation", "")
            
            gaps_for_pdf.append(f"{gap_name}: {explanation}")
            
            st.markdown(f"#### 🎯 Gap {index}: {gap_name}")
            st.caption(f"_{explanation}_")
            
            # Fetch the two prompt options safely
            opt_1 = prompt_dict.get(str(gap.get("option_1_id")))
            opt_2 = prompt_dict.get(str(gap.get("option_2_id")))
            
            # Render Side-by-Side
            col1, col2 = st.columns(2)
            
            with col1:
                if opt_1:
                    flat_pdf_prompts.append(opt_1)
                    with st.expander(f"Option A: {opt_1.get('title')}", expanded=True):
                        st.write(f"**Why use this:** {opt_1.get('description', '')}")
                        st.code(opt_1.get("prompt", ""), language="markdown")
                        if opt_1.get("pro_tips"):
                            for tip in opt_1["pro_tips"]:
                                st.caption(f"- {tip}")
                else:
                    st.warning("Option A prompt data unavailable.")
                    
            with col2:
                if opt_2:
                    flat_pdf_prompts.append(opt_2)
                    with st.expander(f"Option B: {opt_2.get('title')}", expanded=True):
                        st.write(f"**Why use this:** {opt_2.get('description', '')}")
                        st.code(opt_2.get("prompt", ""), language="markdown")
                        if opt_2.get("pro_tips"):
                            for tip in opt_2["pro_tips"]:
                                st.caption(f"- {tip}")
                else:
                    st.warning("Option B prompt data unavailable.")
            
            st.write("---")
            
    else:
        st.error("No strategic gaps were identified. Please check the AI analysis.")

    # 4. THE OPTIMIZATION LOOP INSTRUCTIONS
    st.subheader("🔁 The Optimization Loop")
    st.success(
        """
        **What to do next:**
        1. **Choose:** Pick Option A or Option B for each of your gaps.
        2. **Execute:** Copy the prompts and run them in your preferred AI (ChatGPT, Claude, etc.).
        3. **Apply:** Take the AI's optimized rewrites and update your actual LinkedIn profile.
        4. **Re-Test:** Come back here, click **Start Over**, and run a fresh audit to watch your Profile Health Score climb!
        """
    )
    
    st.write("---")
    
    # 5. PDF & Reset Buttons
    col1, col2 = st.columns(2)
    with col1:
        gaps_string = "\n".join([f"- {g}" for g in gaps_for_pdf])
            
        try:
            pdf_bytes = generate_blueprint_pdf(health_score, gaps_string, flat_pdf_prompts)
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


# import streamlit as st
# import json
# import os
# from utils.pdf_generator import generate_blueprint_pdf

# def load_prompt_library():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(current_dir, "..", "utils", "prompt_library.json")
    
#     if not os.path.exists(file_path):
#         file_path = os.path.join("utils", "prompt_library.json")
        
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             return json.load(file)
#     except Exception:
#         return []

# def render_step5():
#     st.subheader("Step 5: Your AI-Curated Blueprint")
    
#     groq_data = st.session_state.get("groq_analysis", {})
    
#     health_score = groq_data.get("parsed_health_score", "N/A")
#     executive_summary = groq_data.get("executive_summary", "No summary provided.")
#     top_gaps = groq_data.get("top_gaps_explained", ["No gaps identified."])
#     raw_recommended_ids = groq_data.get("recommended_prompt_ids", [])
    
#     # 1. Display Groq's Smart Metrics
#     st.info(f"**Profile Health Score:** {health_score}/100")
#     st.write(f"**Executive Summary:** {executive_summary}")
    
#     st.warning("**Top Critical Gaps:**")
#     for gap in top_gaps:
#         st.markdown(f"- {gap}")
    
#     st.write("---")
#     st.write("### Tactical Rewrite Library")
#     st.write("Based on Groq's semantic analysis, here are the exact prompts to fix your profile.")
    
#     # 2. BULLETPROOF ID MATCHING
#     all_prompts = load_prompt_library()
    
#     safe_recommended_ids = [str(r_id) for r_id in raw_recommended_ids]
    
#     recommended_prompts = [
#         p for p in all_prompts 
#         if str(p.get("id")) in safe_recommended_ids
#     ]
    
#     if not recommended_prompts and all_prompts:
#         recommended_prompts = all_prompts[:min(3, len(all_prompts))]
#         st.caption("*(Note: Default foundational prompts loaded)*")
    
#     # 3. Render Prompts
#     if recommended_prompts:
#         for i, prompt_data in enumerate(recommended_prompts):
#             with st.expander(f"{prompt_data.get('title', 'Prompt')} (Section: {prompt_data.get('section', 'General')})", expanded=(i==0)):
#                 st.write(f"**Why use this:** {prompt_data.get('description', '')}")
#                 st.code(prompt_data.get("prompt", ""), language="markdown")
#                 if prompt_data.get("pro_tips"):
#                     st.caption("**Pro Tips:**")
#                     for tip in prompt_data["pro_tips"]:
#                         st.caption(f"- {tip}")
#     else:
#         st.error("Prompt library is completely empty. Please check your prompt_library.json file.")

#     st.write("---")

#     # 4. THE OPTIMIZATION LOOP INSTRUCTIONS
#     st.subheader("🔁 The Optimization Loop")
#     st.success(
#         """
#         **What to do next:**
#         1. **Execute:** Copy the prompts above and run them in your preferred AI (ChatGPT, Claude, etc.).
#         2. **Apply:** Take the AI's optimized rewrites and update your actual LinkedIn profile.
#         3. **Re-Test:** Once your profile is updated, come back here, click **Start Over**, and run a fresh audit to watch your Profile Health Score climb!
#         """
#     )
    
#     st.write("---")
    
#     # 5. PDF & Reset Buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         # Safely convert top_gaps list into a string for the PDF
#         if isinstance(top_gaps, list):
#             gaps_string = "\n".join([f"- {g}" for g in top_gaps])
#         else:
#             gaps_string = str(top_gaps)
            
#         try:
#             pdf_bytes = generate_blueprint_pdf(health_score, gaps_string, recommended_prompts)
#             st.download_button(
#                 label="📄 Download PDF Blueprint",
#                 data=pdf_bytes,
#                 file_name="LinkedBoost_Blueprint.pdf",
#                 mime="application/pdf",
#                 use_container_width=True
#             )
#         except Exception as e:
#             st.error(f"PDF Generation Error: {e}")
            
#     with col2:
#         if st.button("Start Over (Clear Data)", use_container_width=True):
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.rerun()
