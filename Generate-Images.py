import streamlit as st
from utils.image_generator import generate_image_with_cesdk
from utils.gcs_uploader import save_image_locally
from dotenv import load_dotenv
import os
import json
from pathlib import Path

# Load environment variables
load_dotenv()

st.set_page_config(page_title="🎨 Generate Images", page_icon="🎨")
st.title("🎨 Generate Images with CE.SDK")

# Define input file
enhanced_file = Path("data/enhanced_prompts.json")

if not enhanced_file.exists():
    st.warning("No enhanced prompts found. Please enhance prompts first in Step 2.")
    st.stop()

# Load enhanced prompts
with open(enhanced_file, 'r', encoding='utf-8') as f:
    enhanced_prompts = json.load(f)

st.success(f"Loaded {len(enhanced_prompts)} enhanced prompts.")

# Slider for how many images to generate
limit = st.slider("How many images to generate this round?", min_value=1, max_value=len(enhanced_prompts), value=5)

# Button to begin
if st.button("🖼️ Generate Images"):
    with st.spinner("Generating images using CE.SDK Headless API..."):
        output_dir = Path(os.getenv("OUTPUT_DIRECTORY", "./generated_images"))
        output_dir.mkdir(exist_ok=True)

        results = []
        for prompt in enhanced_prompts[:limit]:
            image_id = prompt['id'].zfill(3)
            prompt_text = prompt['enhanced_prompt']

            # Generate image using CE.SDK
            image_bytes = generate_image_with_cesdk(prompt_text, image_id)
            if image_bytes:
                saved_path = save_image_locally(image_bytes, image_id, output_dir)
                results.append((image_id, saved_path))
            else:
                results.append((image_id, None))

    st.success(f"✅ Done! {len([r for r in results if r[1]])} images generated.")

    for img_id, path in results:
        if path:
            st.image(str(path), caption=f"Image {img_id}", use_column_width=True)
        else:
            st.error(f"❌ Image {img_id} failed to generate.")
