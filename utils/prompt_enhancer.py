import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enhance_prompt(original_prompt: str, scene_type: str) -> str:
    system = {
        "role": "system",
        "content": (
            "You are a professional visual content prompt engineer. "
            "Enhance the user's image prompt with visual storytelling, "
            "consistent style, emotional tone, and origami stickman aesthetics. "
            "Style: pastel paper textures, emotional symbolism, minimalist depth."
        )
    }

    user = {
        "role": "user",
        "content": f"""
        Enhance this image prompt for consistent brand style:

        Original: {original_prompt}
        Scene Type: {scene_type}

        Aesthetic Guide: Origami-folded paper stickman, pastel tones, soft lighting, emotional clarity.
        Keep the mood and meaning intact.

        Return only the improved prompt.
        """
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[system, user],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Prompt Enhancement Failed] {str(e)}"
