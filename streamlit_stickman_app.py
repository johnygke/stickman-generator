import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from utils.csv_loader import load_csv_prompts
from utils.prompt_enhancer import enhance_prompt
from utils.image_generator import generate_image
from utils.gcs_uploader import upload_to_gcs

# Load environment variables
load_dotenv()
OUTPUT_DIR = os.getenv("OUTPUT_DIRECTORY", "./generated_images")
BUCKET_NAME = os.getenv("GOOGLE_CLOUD_BUCKET")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))
REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", 3))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

st.set_page_config(page_title="Stickman Origami Generator", layout="centered")
st.title("🧠 Stickman Origami Generator with GPT-Image-1 + GCS")

st.markdown("### Generate consistent pastel stickman illustrations powered by GPT-4o and OpenAI Image API.")
st.markdown("""
1. **Upload Prompts** (from CSV)
2. **Enhance** using GPT-4o
3. **Generate Images** (via GPT-Image-1)
4. **Upload to Cloud** (Google Cloud Storage)
""")

st.divider()
with st.form("image_form"):
    image_id = st.text_input("Image ID", value="001")
    original_prompt = st.text_area("Original Prompt", height=120)
    scene_type = st.selectbox("Scene Category", ["mental health", "emotion", "recovery", "relationships"])
    submitted = st.form_submit_button("⚡ Generate Image")

if submitted:
    if not original_prompt.strip():
        st.warning("Please enter a prompt before generating.")
    else:
        with st.spinner("Enhancing prompt with GPT-4o..."):
            enhanced_prompt = enhance_prompt(original_prompt, scene_type)

        with st.spinner("Generating image using GPT-Image-1..."):
            image_path = generate_image(prompt=enhanced_prompt, image_id=image_id, output_dir=OUTPUT_DIR)

        with st.spinner("Uploading to Google Cloud Storage..."):
            gcs_path = upload_to_gcs(image_path, BUCKET_NAME, CREDENTIALS_PATH, PROJECT_ID)
            st.success("Upload complete!")
            st.image(image_path, caption="Generated Stickman Illustration", use_column_width=True)
            st.write(f"GCS Path: `{gcs_path}`")