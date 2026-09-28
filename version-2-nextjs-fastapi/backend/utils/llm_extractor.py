import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"  # or mistral/llama3

PROMPT = """
You are an expert resume parser.

Extract structured data from the resume text.

Return STRICT JSON ONLY in this format:
{
  "skills": ["..."],
  "experience_years": number,
  "education": "...",
  "keywords": ["..."]
}

Guidelines:
- Infer skills semantically (e.g., "built models" -> "machine learning")
- Normalize skills to short phrases
- Do not include explanations, only JSON
"""

def extract_with_llm(text: str):
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": PROMPT + "\n\nResume:\n" + text,
                "stream": False
            },
            timeout=120,
        )
        raw = resp.json().get("response", "")

        # isolate JSON block
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        # basic guards
        return {
            "skills": [s.lower() for s in data.get("skills", [])],
            "experience_years": data.get("experience_years", 0),
            "education": data.get("education", "Unknown"),
            "keywords": [k.lower() for k in data.get("keywords", [])],
        }

    except Exception:
        # safe fallback
        return {
            "skills": [],
            "experience_years": 0,
            "education": "Unknown",
            "keywords": []
        }