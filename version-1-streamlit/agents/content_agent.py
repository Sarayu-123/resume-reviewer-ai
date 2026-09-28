import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi"   # Change to "mistral" if system is powerful


def extract_bullets(text):
    bullets = []

    parts = text.split("•")

    for part in parts:
        cleaned = part.strip()
        if len(cleaned.split()) >= 6:
            bullets.append(cleaned)

    return bullets


def analyze_bullets_with_ai(bullets):
    if not bullets:
        return ""

    full_response = ""

    for bullet in bullets[:5]:  # limit for performance
        prompt = f"""
You are a strict resume reviewer.

Bullet:
{bullet}

1. Identify what is weak or missing.
2. Suggest a stronger rewritten version with quantification and impact.

Be concise.
"""

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=180
            )

            result = response.json().get("response", "")
            full_response += f"\n### Original:\n{bullet}\n\n{result}\n\n---\n"

        except Exception as e:
            full_response += f"\nError analyzing bullet:\n{bullet}\n{e}\n\n"

    return full_response