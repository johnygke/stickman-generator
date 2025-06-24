# pages/1_📤_Upload_Prompts.py
import streamlit as st
from utils.csv_loader import load_and_preview_csv
from pathlib import Path

st.set_page_config(page_title="📤 Upload Prompts", layout="wide")
st.title("Step 1: 📤 Upload Your Prompt CSV")

st.markdown("""
Upload a CSV file containing your stickman prompt entries. 
Make sure it includes the following headers:
- **ID**
- **Original_Prompt**
- **Scene_Category**
- **Mood_Tone**
- **Story_Arc**
""")

uploaded_file = st.file_uploader("Choose your prompt CSV", type=["csv"])

if uploaded_file is not None:
    prompts_df = load_and_preview_csv(uploaded_file)
    st.success(f"Successfully loaded {len(prompts_df)} prompts!")
    st.dataframe(prompts_df, use_container_width=True)

    # Save uploaded file to session state
    st.session_state["uploaded_prompts"] = prompts_df

    # Optional: Save a local copy to your project folder
    save_path = Path("./uploaded_prompts.csv")
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.info(f"Saved a copy to: `{save_path}`")
