import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi"


def generate_suggestions(text):

    prompt = f"""
You are a strict resume reviewer.

Analyze the resume and give 3 improvement suggestions.

Resume:
{text}

Format:

Title: ...
Description: ...
"""

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        result = data.get("response", "")

        suggestions = []

        parts = result.split("Title:")

        for part in parts:

            if "Description:" in part:

                title = part.split("Description:")[0].strip()

                desc = part.split("Description:")[1].strip()

                suggestions.append({
                    "title": title,
                    "description": desc
                })

        if len(suggestions) == 0:

            suggestions.append({
                "title": "Resume Improvement",
                "description": "Add measurable achievements and clearer bullet points."
            })

        return suggestions

    except Exception as e:

        return [{
            "title": "AI unavailable",
            "description": str(e)
        }]