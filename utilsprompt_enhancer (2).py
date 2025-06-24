import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def enhance_prompt(original_prompt: str, category: str = "mental health") -> str:
    """
    Enhance a base image prompt using GPT-4o for better visual storytelling.
    Optionally include a category to guide enhancement context.
    """
    system_message = (
        "You are a visual prompt enhancer for mental health storytelling.
         Your job is to turn simple prompts into vivid, emotionally resonant image descriptions in the style of origami folded paper stickmen.")

    user_message = f"""
    Original prompt:
    "{original_prompt}"

    Category: {category}

    Please rewrite this prompt into a vivid, visually rich description for AI image generation.
    Emphasize emotional tone, body language, facial expression, and setting.
    Limit to 1 paragraph. End with: "16:9 landscape".
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        enhanced = response.choices[0].message["content"].strip()
        return enhanced
    except Exception as e:
        print(f"Error enhancing prompt: {e}")
        return original_prompt
