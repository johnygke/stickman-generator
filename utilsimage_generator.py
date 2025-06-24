import os
import base64
import json
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_DIR = os.getenv("OUTPUT_DIRECTORY", "./generated_images")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_image(prompt: str, image_id: str, category: str = "default") -> str:
    """
    Calls the GPT-Image-1 API (via OpenAI image API) to generate an image from a prompt.
    Saves the image locally and returns the file path.
    """
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "dall-e-3",  # Temporarily using this endpoint until GPT-Image-1 has API access
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    image_data = response.json()["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_data)
    
    file_name = f"{category}_{image_id}.png"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path

def generate_batch(prompts: list, category: str = "default") -> list:
    """
    Generates images from a batch of prompts and returns list of image paths.
    """
    image_paths = []
    for idx, prompt in enumerate(prompts):
        image_id = str(idx + 1).zfill(3)
        try:
            img_path = generate_image(prompt, image_id, category)
            image_paths.append(img_path)
        except Exception as e:
            print(f"❌ Failed to generate image for prompt {image_id}: {e}")
    return image_paths
