from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import openai
import requests
import json
from google.cloud import storage
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# --- LOAD ENV ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
CE_API_KEY = os.getenv("CE_API_KEY")
GCS_BUCKET = os.getenv("GOOGLE_CLOUD_BUCKET")
GCS_CREDS = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")

# --- CONFIG ---
st.set_page_config(page_title="Stickman Generator", layout="centered")
st.title("🧠 Stickman Origami Generator with GPT-Image-1 + GCS")

# --- INPUT FORM ---
with st.form("image_form"):
    id = st.text_input("Image ID", value="001")
    original_prompt = st.text_area("Original Prompt", height=150)
    scene_type = st.selectbox("Scene Category", ["mental health", "philosophical", "parenting", "self-worth", "symbolic"])
    submit = st.form_submit_button("✨ Generate Image")

# --- STYLE GUIDE FOR GPT-4o ---
STYLE_GUIDE = """
Style Guide: Origami-folded paper aesthetic with clean geometric lines, 
soft pastel colors (beige #F5E6D3, warm gray #E8D5B7, muted blue #B5A584), 
minimalist composition, emotional depth, 16:9 landscape format,
paper-like textures, gentle lighting, artistic shadows.
"""

# --- HELPER: Prompt Enhancer ---
def enhance_prompt(prompt, category):
    system = {"role": "system", "content": "You are a world-class prompt engineer."}
    user = {"role": "user", "content": f"Enhance the following prompt for consistency with our brand style:\n\nPrompt: {prompt}\nCategory: {category}\n\n{STYLE_GUIDE}\n\nReturn only the enhanced image prompt."}
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[system, user],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- HELPER: Call CE.SDK API ---
def call_cesdk(prompt, image_id):
    headers = {
        "Authorization": f"Bearer {CE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "n": 1,
        "size": "1792x1024",
        "model": "image-1"
    }
    response = requests.post("https://api.cesdk.app/v1/images/generate", headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data['images'][0]['url']
    else:
        st.error(f"❌ CE.SDK Error: {response.status_code}")
        return None

# --- HELPER: Upload to GCS ---
def upload_to_gcs(local_path, image_id):
    client = storage.Client.from_service_account_json(GCS_CREDS)
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(f"origami_stickman/{image_id}.png")
    blob.upload_from_filename(local_path)
    return blob.public_url

# --- MAIN EXECUTION ---
if submit and original_prompt:
    with st.spinner("🔍 Enhancing prompt with GPT-4o..."):
        enhanced = enhance_prompt(original_prompt, scene_type)
        st.text_area("🧠 Enhanced Prompt", value=enhanced, height=120)

    with st.spinner("🎨 Generating image with CE.SDK..."):
        img_url = call_cesdk(enhanced, id)

    if img_url:
        st.image(img_url, caption="Preview (Click right to save)")

        # Download locally
        local_path = Path(f"generated_{id}.png")
        with open(local_path, 'wb') as f:
            f.write(requests.get(img_url).content)

        with st.spinner("☁️ Uploading to Google Cloud Storage..."):
            public_url = upload_to_gcs(local_path, id)
            st.success("✅ Uploaded to GCS")
            st.markdown(f"📂 [View on GCS]({public_url})")

        # Save metadata
        meta = {
            "id": id,
            "original_prompt": original_prompt,
            "enhanced_prompt": enhanced,
            "scene": scene_type,
            "image_url": img_url,
            "gcs_url": public_url,
            "generated": datetime.now().isoformat()
        }
        with open(f"metadata_{id}.json", "w") as f:
            json.dump(meta, f, indent=2)

        st.download_button("📥 Download Metadata JSON", data=json.dumps(meta, indent=2), file_name=f"metadata_{id}.json")
