# utils/csv_loader.py
import pandas as pd
import streamlit as st

REQUIRED_COLUMNS = ['ID', 'Original_Prompt', 'Scene_Category', 'Mood_Tone', 'Story_Arc']

def load_and_preview_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            return pd.DataFrame()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")
        return pd.DataFrame()
