
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def enhance_prompt(original_prompt, scene_type):
    try:
        system = {
            "role": "system",
            "content": "You are a prompt enhancer for origami stickman illustrations. Add emotional and visual depth."
        }
        user = {
            "role": "user",
            "content": f"Enhance this prompt for a {scene_type} scene:\n\n{original_prompt}"
        }
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[system, user],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Prompt Enhancement Failed] {str(e)}"
