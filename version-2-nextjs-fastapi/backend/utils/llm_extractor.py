"""Conservative resume information extraction through a local Ollama model."""

import json
import logging
import math
import re

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

logger = logging.getLogger(__name__)

PROMPT = r"""
Extract structured information from the resume below. Return valid JSON only.
Use exactly this schema:
{
  "skills": [],
  "experience_years": null,
  "education": "Unknown",
  "keywords": []
}

EXPERIENCE RULES — FOLLOW STRICTLY:
- experience_years means total PROFESSIONAL EMPLOYMENT experience only.
- Count explicitly supported professional employment such as full-time, part-time, or contract jobs. Count freelance/self-employed work only when the resume clearly presents it as professional work and provides enough dates to estimate duration.
- Do NOT count internships, academic training, college or personal projects, coursework, volunteering, certifications, or years spent studying.
- Do not count an internship even if it has start and end dates. Do not combine internship duration with employment duration.
- Use dates only when they are explicitly present in the resume. Do not invent or infer missing start/end dates.
- When employment dates are provided, estimate total professional employment duration from those dates. Do not double-count overlapping employment periods.
- If the resume clearly indicates a fresher or explicitly indicates no professional employment experience, return 0.
- If employment status or dates are insufficient to determine total professional experience, return null. Do not return 0 merely because the resume has no experience section or because extraction is uncertain.
- A project, internship, or education entry alone does not establish professional employment experience.

OTHER RULES:
- Extract skills and keywords only when supported by the resume.
- Education may be a string or an object containing course/degree and institution.
- Do not invent skills, qualifications, employers, or dates.
- Return JSON only, with no Markdown fences or explanation.
"""


def _fallback() -> dict:
    return {
        "skills": [],
        "experience_years": None,
        "education": "Unknown",
        "keywords": [],
    }


def _clean_string_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    cleaned = []
    seen = set()
    for item in value:
        if isinstance(item, str) and item.strip():
            normalized = re.sub(r"\s+", " ", item.strip().lower())
            if normalized not in seen:
                seen.add(normalized)
                cleaned.append(normalized)
    return cleaned


def extract_with_llm(text: str) -> dict:
    """Extract resume fields; experience_years is professional employment only."""
    fallback = _fallback()
    if not isinstance(text, str) or not text.strip():
        return fallback

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": PROMPT + "\n\nRESUME TEXT:\n" + text[:12000],
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )
        response.raise_for_status()
        raw_response = response.json().get("response", "")
        data = json.loads(raw_response)
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object from Ollama")

        experience = data.get("experience_years")
        if isinstance(experience, bool) or experience is None:
            experience = None
        else:
            try:
                experience = float(experience)
                if not math.isfinite(experience) or experience < 0 or experience > 60:
                    experience = None
            except (TypeError, ValueError, OverflowError):
                experience = None

        education = data.get("education", "Unknown")
        if not isinstance(education, (str, dict)) or not education:
            education = "Unknown"

        return {
            "skills": _clean_string_list(data.get("skills")),
            "experience_years": experience,
            "education": education,
            "keywords": _clean_string_list(data.get("keywords")),
        }

    except (requests.RequestException, ValueError, TypeError, KeyError) as error:
        logger.exception("Ollama extraction failed: %s", error)
        return fallback
