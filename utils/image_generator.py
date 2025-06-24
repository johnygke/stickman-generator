import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt: str, image_id: str, output_dir: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
        output_path = os.path.join(output_dir, f"{image_id}.png")

        img_data = requests.get(image_url).content
        with open(output_path, "wb") as f:
            f.write(img_data)

        return output_path

    except Exception as e:
        return f"[Image Generation Failed] {str(e)}"
