
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image_from_prompt(prompt, image_id):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(f"[Image Generation Failed] {str(e)}")
        return None
