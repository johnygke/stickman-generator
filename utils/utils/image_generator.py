from openai import OpenAI
import requests

client = OpenAI()

def generate_image(prompt: str, image_id: str, output_dir: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1792x1024",
            quality="hd",
            response_format="url"
        )

        image_url = response.data[0].url

        if not image_url:
            return ""

        image_path = f"{output_dir}/{image_id}.png"
        with requests.get(image_url, stream=True) as r:
            r.raise_for_status()
            with open(image_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return image_path

    except Exception as e:
        return ""