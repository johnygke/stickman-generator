# /pages/2_✨_Enhance_Prompts.py
import streamlit as st
from utils.gpt_enhancer import enhance_prompt
from utils.session_state import init_session

st.set_page_config(page_title="✨ Enhance Prompts", page_icon="✨")

init_session()

st.title("🌟 Enhance Prompts with GPT-4o")

if not st.session_state.get("prompts"):
    st.warning("🚨 No prompts found. Please upload prompts first on the previous page.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.write("### Original Prompt")
    st.text_area("Prompt", st.session_state["prompts"][0]["original_prompt"], height=200, disabled=True)

with col2:
    st.write("### Enhanced Prompt")
    if st.button("Enhance All Prompts 🔄"):
        with st.spinner("Calling GPT-4o..."):
            for p in st.session_state["prompts"]:
                p["enhanced_prompt"] = enhance_prompt(p["original_prompt"], p["scene_category"]) 
        st.success("Prompts enhanced successfully!")

if st.session_state.get("prompts"):
    st.dataframe(
        [{"Image ID": p["image_id"], "Original": p["original_prompt"], "Enhanced": p["enhanced_prompt"]} 
         for p in st.session_state["prompts"] if p.get("enhanced_prompt")], 
        use_container_width=True
    )
