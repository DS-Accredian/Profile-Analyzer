import streamlit as st
import os

# Set page config FIRST
st.set_page_config(page_title="LinkedBoost BYO-AI", layout="wide", page_icon="🚀")

# Import Step Components
from components.step1 import render_step1
from components.step2 import render_step2
from components.step3 import render_step3
from components.step4 import render_step4
from components.step5 import render_step5

# Load Custom CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles/style.css")

# Initialize Routing State
if "step" not in st.session_state:
    st.session_state["step"] = 1

# Core Routing Logic
def main():
    st.title("🚀 LinkedBoost")
    
    step = st.session_state["step"]
    
    if step == 1:
        render_step1()
    elif step == 2:
        render_step2()
    elif step == 3:
        render_step3()
    elif step == 4:
        render_step4()
    elif step == 5:
        render_step5()

if __name__ == "__main__":
    main()
