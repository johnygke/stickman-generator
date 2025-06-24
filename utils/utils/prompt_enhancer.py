from openai import OpenAI

client = OpenAI()

def enhance_prompt(original_prompt: str, scene_type: str) -> str:
    system = {
        "role": "system",
        "content": "You are an expert prompt engineer for visual content creation."
    }
    user = {
        "role": "user",
        "content": f"""
Enhance this image prompt for consistent brand style:

Original: {original_prompt}
Scene Type: {scene_type}

Style Guide: Origami-folded paper aesthetic with clean geometric lines, 
soft pastel colors (beige #F5E6D3, warm gray #E8D5B7, muted blue #B5A584), 
minimalist composition, emotional depth, 16:9 landscape format,
paper-like textures, gentle lighting, artistic shadows.

Create a detailed, vivid description that maintains the origami paper aesthetic 
while adding rich visual details, emotional depth, and cinematic composition.
Keep the core story and mood intact.

Return only the enhanced prompt, no explanation.
"""
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[system, user],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return original_prompt