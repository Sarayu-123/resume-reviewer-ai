
"""FastAPI backend for Resume Reviewer AI."""

import io
import json
import logging
import os
import re

import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from utils.pdf_reader import read_pdf
from utils.docx_reader import read_docx
from utils.llm_extractor import extract_with_llm
from utils.jd_analyzer import analyze_jd_relevance


logger = logging.getLogger(__name__)

app = FastAPI(title="Resume Reviewer AI")

# Configure FRONTEND_ORIGINS as a comma-separated list when deploying.
# Local development defaults cover common Next.js ports.
FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    # Also permit the local LAN origin used by some Next.js dev setups.
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|192\.168\.56\.1)(:\d+)?",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


# --------------------------------------------------
# ROLE REQUIREMENTS
# --------------------------------------------------

ROLE_SKILLS = {
    "Frontend Developer": [
        "html", "css", "javascript", "react", "next.js", "tailwind"
    ],
    "Backend Developer": [
        "python", "java", "node", "sql", "api", "django", "flask"
    ],
    "Fullstack Developer": [
        "react", "node", "python", "sql", "api", "javascript"
    ],
    "Data Scientist": [
        "python", "pandas", "numpy", "machine learning", "statistics"
    ],
    "Machine Learning Engineer": [
        "python", "tensorflow", "pytorch", "deep learning"
    ],
    "Data Engineer": [
        "sql", "etl", "spark", "hadoop", "pipeline"
    ],
    "Data Analyst": [
        "sql", "excel", "power bi", "tableau", "python"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "aws", "ci/cd", "linux"
    ],
    "Cloud Engineer": [
        "aws", "azure", "gcp", "cloud", "terraform"
    ],
    "Mobile Developer": [
        "android", "ios", "flutter", "react native"
    ],
    "AI Engineer": [
        "python", "nlp", "llm", "machine learning"
    ],
    "Software Engineer": [
        "python", "java", "c++", "sql", "git"
    ],
    "Product Manager": [
        "roadmap", "agile", "scrum", "stakeholder"
    ],
    "UX Designer": [
        "figma", "wireframe", "ux", "ui"
    ],
    "Security Engineer": [
        "security", "network", "encryption"
    ],
    "QA Engineer": [
        "testing", "selenium", "automation"
    ],
}


# --------------------------------------------------
# SKILL NORMALIZATION
# --------------------------------------------------

SKILL_ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "node.js": "node",
    "nodejs": "node",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "machine-learning": "machine learning",
    "deep-learning": "deep learning",
    "natural language processing": "nlp",
    "large language models": "llm",
    "large language model": "llm",
    "structured query language": "sql",
    "powerbi": "power bi",
    "power-bi": "power bi",
    "tailwind css": "tailwind",
    "nextjs": "next.js",
    "c plus plus": "c++",
    "natural-language processing": "nlp",
}


def normalize_skill(skill: str) -> str:
    """Normalize common skill-name variations to a canonical skill name."""
    value = re.sub(r"\s+", " ", skill.lower().strip())
    return SKILL_ALIASES.get(value, value)


ALL_SKILLS = {
    normalize_skill(skill)
    for skills in ROLE_SKILLS.values()
    for skill in skills
}


# --------------------------------------------------
# KEYWORD EXTRACTION
# --------------------------------------------------

def extract_keywords(text: str) -> set:
    """Find predefined role skills explicitly mentioned in resume text."""
    found = set()
    text = text.lower()

    # Search canonical names and known aliases, but always store canonical names.
    candidates = set(ALL_SKILLS) | set(SKILL_ALIASES.keys())
    for candidate in candidates:
        pattern = rf"(?<!\w){re.escape(candidate)}(?!\w)"
        if re.search(pattern, text):
            found.add(normalize_skill(candidate))

    return found


# --------------------------------------------------
# HYBRID SKILL MATCHING
# --------------------------------------------------

def match_skills(text: str, role: str):
    """Combine deterministic keyword matching with Ollama extraction."""
    if role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role: {role}",
        )

    role_skills = ROLE_SKILLS[role]

    keyword_skills = extract_keywords(text)

    llm_data = extract_with_llm(text)
    if not isinstance(llm_data, dict):
        llm_data = {
            "skills": [], "experience_years": None,
            "education": "Unknown", "keywords": [],
        }

    logger.info("Ollama extracted data: %s", llm_data)

    raw_llm_skills = llm_data.get("skills", [])
    if not isinstance(raw_llm_skills, list):
        raw_llm_skills = []
    llm_skills = {
        normalize_skill(skill)
        for skill in raw_llm_skills
        if isinstance(skill, str)
    }

    # The LLM may help interpret the resume, but it cannot establish a skill
    # without textual evidence. This prevents hallucinated skills being marked found.
    evidence_backed_llm_skills = llm_skills & keyword_skills
    matches = []

    for skill in role_skills:
        required = normalize_skill(skill)
        found = required in keyword_skills

        if required in keyword_skills and required in evidence_backed_llm_skills:
            source = "keyword_and_llm"
        elif required in keyword_skills:
            source = "keyword"
        else:
            source = "not_detected"

        matches.append({
            "skill": skill.title(),
            "match": 100 if found else 0,
            "found": found,
            "source": source,
        })

    total = len(matches)
    matched_count = sum(item["found"] for item in matches)

    coverage_score = (
        round(matched_count * 100 / total)
        if total
        else 0
    )

    found_skills = [
        item["skill"].lower()
        for item in matches
        if item["found"]
    ]

    missing_skills = [
        item["skill"].lower()
        for item in matches
        if not item["found"]
    ]

    return (
        matches,
        coverage_score,
        found_skills,
        missing_skills,
        llm_data,
    )


# --------------------------------------------------
# EDUCATION FORMATTING
# --------------------------------------------------

def format_education(education) -> str:
    """Format education data returned by the LLM."""
    if isinstance(education, dict):
        course = (
            education.get("degree")
            or education.get("course")
            or "Unknown"
        )

        institution = education.get("institution") or ""

        if institution:
            return f"{course} ({institution})"

        return course

    if isinstance(education, str) and education.strip():
        return education.strip()

    return "Unknown"


# --------------------------------------------------
# EXPERIENCE RELEVANCE AND EDUCATION MATCH
# --------------------------------------------------

ROLE_EDUCATION_TERMS = {
    "Frontend Developer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "web development", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Backend Developer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "bachelor of technology", "b.tech", "b.e.",
            ],
    "Fullstack Developer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "bachelor of technology", "b.tech", "b.e.",
            ],
    "Software Engineer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "information systems", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Data Scientist": [
        "computer science", "data science", "statistics", "mathematics",
        "artificial intelligence", "machine learning", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Machine Learning Engineer": [
        "computer science", "artificial intelligence", "machine learning",
        "data science", "information technology", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Data Engineer": [
        "computer science", "data engineering", "information technology",
        "information systems", "bachelor of technology", "b.tech", "b.e.",
            ],
    "Data Analyst": [
        "data analytics", "data science", "statistics", "mathematics",
        "economics", "computer science", "information technology",
        "bachelor of technology", "b.tech", "b.e."
    ],
    "DevOps Engineer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "bachelor of technology", "b.tech", "b.e.",
            ],
    "Cloud Engineer": [
        "computer science", "computer engineering", "information technology",
        "cloud computing", "software engineering", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Mobile Developer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "bachelor of technology", "b.tech", "b.e.",
            ],
    "AI Engineer": [
        "computer science", "artificial intelligence", "machine learning",
        "data science", "information technology", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "Product Manager": [
        "business administration", "management", "business",
        "computer science", "information technology", "mba"
    ],
    "UX Designer": [
        "design", "human-computer interaction", "interaction design",
        "visual communication", "computer science"
    ],
    "Security Engineer": [
        "cybersecurity", "information security", "computer science",
        "information technology", "network security", "bachelor of technology",
        "b.tech", "b.e."
    ],
    "QA Engineer": [
        "computer science", "computer engineering", "information technology",
        "software engineering", "bachelor of technology", "b.tech", "b.e.",
            ],
}


def calculate_experience_relevance(resume_text: str, role: str, skills: list) -> int:
    """Estimate role relevance from detected role skills, not years of employment.

    This is a skill-evidence heuristic and must not be interpreted as verified
    professional experience or employment duration.
    """
    role_skills = ROLE_SKILLS.get(role, [])
    if not role_skills:
        return 0

    found_by_name = {
        normalize_skill(item.get("skill", ""))
        for item in skills
        if isinstance(item, dict) and item.get("found") is True
        and isinstance(item.get("skill"), str)
    }
    matched_count = sum(
        1 for required in role_skills
        if normalize_skill(required) in found_by_name
    )
    return round(matched_count * 100 / len(role_skills))


def calculate_education_match(education, role: str) -> int:
    """Return 100 for a role-related field, 50 for a clearly technical degree,
    and 0 when education is unknown or relevance is not detected. This is a
    heuristic based on extracted education text, not credential verification.
    """
    degree_text = format_education(education)
    if degree_text == "Unknown":
        return 0

    degree_lower = re.sub(r"\s+", " ", degree_text.lower()).strip()
    role_terms = ROLE_EDUCATION_TERMS.get(role, [])
    for term in role_terms:
        normalized_term = re.sub(r"\s+", " ", term.lower()).strip()
        if re.search(rf"(?<!\w){re.escape(normalized_term)}(?!\w)", degree_lower):
            return 100

    # Generic computing/engineering degrees are partially relevant to many
    # technical roles, but are not treated as a perfect role-specific match.
    technical_terms = (
        "computer", "computing", "information technology", "software",
        "engineering", "data", "statistics", "mathematics", "cyber",
        "artificial intelligence", "business administration", "design",
    )
    if any(re.search(rf"(?<!\w){re.escape(term)}(?!\w)", degree_lower)
           for term in technical_terms):
        return 50
    return 0


# --------------------------------------------------
# AI SUGGESTIONS
# --------------------------------------------------


def generate_resume_suggestions(role, skills, resume_text):
    """Generate concise suggestions and reject obvious unsupported metrics."""
    if role not in ROLE_SKILLS:
        raise ValueError(f"Unsupported role for suggestions: {role}")

    if not isinstance(resume_text, str) or not resume_text.strip():
        return []

    normalized_skills = []
    for item in skills:
        if not isinstance(item, dict) or not isinstance(item.get("skill"), str):
            continue
        normalized_skills.append({
            "skill": item["skill"],
            "found": bool(item.get("found", False)),
            "source": item.get("source", "not_detected"),
        })

    missing = [item["skill"] for item in normalized_skills if not item["found"]]
    found = [item["skill"] for item in normalized_skills if item["found"]]

    prompt = f"""
You are a conservative, evidence-based resume reviewer.

Target role: {role}
Detected required skills: {json.dumps(found)}
Requirements not detected by the analyzer: {json.dumps(missing)}
Resume text (the only source of candidate-specific facts):
{resume_text[:12000]}

Return valid JSON only:
{{
  "suggestions": [
    {{"title": "Short actionable title", "description": "Specific recommendation"}}
  ]
}}

Rules:
- Return only useful recommendations for this resume and target role; any number is allowed, including zero.
- Treat the resume text as the only evidence for facts about this candidate.
- A skill marked not detected may be absent from the resume or missed by extraction. Phrase it as "not detected" rather than asserting the candidate does not know it.
- You may recommend learning a relevant missing skill or building a project to demonstrate it.
- Never invent or imply candidate achievements, employers, dates, education, responsibilities, project names, project implementations, metrics, or results.
- Never create example resume bullets that state unverified facts.
- Never include a percentage, count, speed improvement, accuracy value, or other numeric achievement unless that exact result is present in the resume text.
- Do not assume a project used a technology unless the resume says so.
- Do not recommend adding a dedicated section unless the resume text supports that the section is missing.
- Prefer specific actions over generic statements such as "improve your skills".
- Do not repeat the same recommendation in different words.
- Keep each suggestion concise and actionable.
- Return an empty list when no defensible recommendation is useful.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )
    response.raise_for_status()

    result = json.loads(response.json().get("response", ""))
    suggestions = result.get("suggestions", []) if isinstance(result, dict) else []
    if not isinstance(suggestions, list):
        raise ValueError("Invalid suggestions format from Ollama")

    # Numbers in generated suggestions can be invented achievements. Reject a
    # suggestion if it contains a numeric token not found in the resume text.
    resume_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?%?\b", resume_text))
    validated = []
    seen = set()

    for item in suggestions:
        if not isinstance(item, dict):
            continue

        title = item.get("title")
        description = item.get("description")
        if not isinstance(title, str) or not isinstance(description, str):
            continue

        title = title.strip()
        description = description.strip()
        if not title or not description:
            continue

        combined = f"{title} {description}"
        generated_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?%?\b", combined))
        if generated_numbers - resume_numbers:
            logger.warning("Rejected suggestion containing unsupported numeric claims")
            continue

        dedupe_key = re.sub(r"\W+", " ", f"{title} {description}".lower()).strip()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        validated.append({"title": title, "description": description})

    return validated


# --------------------------------------------------
# BASIC ATS READABILITY CHECKS
# --------------------------------------------------

def calculate_ats_score(resume_text: str) -> tuple[int, dict]:
    """Estimate text readability and common resume structure. Not a real ATS test.

    Does not penalize a fresher for having no employment-history section and does
    not include job-fit/skill coverage, which is scored separately.
    """
    text = resume_text.strip()
    lower = text.lower()
    nonempty_lines = [line for line in text.splitlines() if line.strip()]

    checks = {
        "email_detected": bool(re.search(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text, re.I)),
        "phone_detected": bool(re.search(
            r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)", text)),
        "education_section": bool(re.search(r"\beducation\b", lower)),
        "skills_section": bool(re.search(
            r"\b(technical skills|skills|technical proficiencies)\b", lower)),
        "summary_or_objective": bool(re.search(
            r"\b(summary|professional summary|objective|career objective|profile)\b", lower)),
        "projects_or_experience_section": bool(re.search(
            r"\b(projects?|professional experience|work experience|employment history|work history|internships?)\b", lower)),
        "readable_length": 300 <= len(text) <= 20000,
        "structured_lines": len(nonempty_lines) >= 8,
    }
    weights = {
        "email_detected": 15,
        "phone_detected": 10,
        "education_section": 15,
        "skills_section": 15,
        "summary_or_objective": 10,
        "projects_or_experience_section": 15,
        "readable_length": 10,
        "structured_lines": 10,
    }
    score = sum(weights[key] for key, passed in checks.items() if passed)
    return score, {
        key: {"passed": passed, "weight": weights[key]}
        for key, passed in checks.items()
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    """Confirm that the backend is running."""
    return {"message": "Hybrid AI backend running"}


@app.get("/health")
def health():
    """Lightweight health endpoint for local frontend/backend diagnostics."""
    return {"status": "ok", "service": "resume-reviewer-api"}


# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    role: str = Form(...),
):
    """Extract resume information and calculate skill coverage."""
    filename = (file.filename or "").lower()

    if role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role: {role}",
        )

    if not filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF or DOCX file",
        )

    # Enforce the limit on actual bytes read; UploadFile.size may be unavailable.
    raw_file = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw_file) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Resume file is too large. Maximum allowed size is 10 MB.",
        )
    if not raw_file:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

    # Validate the basic file signature instead of trusting only the extension.
    try:
        if filename.endswith(".pdf"):
            if not raw_file.startswith(b"%PDF-"):
                raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF")
            text = await run_in_threadpool(read_pdf, io.BytesIO(raw_file))
        else:
            if not raw_file.startswith(b"PK\x03\x04"):
                raise HTTPException(status_code=400, detail="The uploaded file is not a valid DOCX")
            text = await run_in_threadpool(read_docx, io.BytesIO(raw_file))
    except HTTPException:
        raise
    except ValueError as error:
        logger.warning("Resume parsing failed for %s: %s", filename, error)
        raise HTTPException(status_code=422, detail=str(error)) from error

    if not isinstance(text, str) or not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the uploaded resume",
        )

    (
        skill_matches,
        coverage_score,
        found_skills,
        missing_skills,
        llm_data,
    ) = await run_in_threadpool(match_skills, text, role)

    if not isinstance(llm_data, dict):
        llm_data = {
            "skills": [], "experience_years": None,
            "education": "Unknown", "keywords": [],
        }

    education = format_education(llm_data.get("education"))

    experience_years = llm_data.get("experience_years")
    if isinstance(experience_years, bool) or not isinstance(experience_years, (int, float)):
        experience_years = None
    elif experience_years < 0 or experience_years > 60:
        experience_years = None
    else:
        experience_years = round(float(experience_years), 1)

    experience_relevance = calculate_experience_relevance(
        text, role, skill_matches
    )
    education_match = calculate_education_match(
        llm_data.get("education"), role
    )
    ats_score, ats_breakdown = calculate_ats_score(text)

    return {
        "overallScore": coverage_score,
        "role": role,
        "fileName": file.filename,
        "resumeText": text[:8000],

        "experience": {
            "years": experience_years,
            "known": experience_years is not None,
            "type": "professional_employment_only",
            "relevance": experience_relevance,  # Backward-compatible frontend field
            "relevanceLabel": "role_skill_coverage_not_years_of_experience",
        },

        "education": {
            "degree": education,
            "match": education_match,
        },

        "keywords": {
            "found": len(found_skills),
            "missing": len(missing_skills),
        },

        "atsScore": ats_score,
        "atsBreakdown": ats_breakdown,
        "skillMatches": skill_matches,
    }


# --------------------------------------------------
# AI SUGGESTIONS ENDPOINT
# --------------------------------------------------

@app.post("/ai-suggestions")
async def ai_suggestions(data: dict):
    """Generate suggestions from resume evidence using Ollama."""
    role = data.get("role", "")
    skills = data.get("skillMatches", [])
    resume_text = data.get("resumeText", "")

    if role not in ROLE_SKILLS or not isinstance(skills, list):
        raise HTTPException(
            status_code=400,
            detail="A supported role and a skillMatches list are required",
        )

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is required for AI suggestions",
        )

    try:
        suggestions = await run_in_threadpool(
            generate_resume_suggestions,
            role,
            skills,
            resume_text,
        )

        return {"suggestions": suggestions}

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
    ) as error:
        logger.exception(
            "AI suggestion generation failed: %s",
            error,
        )

        raise HTTPException(
            status_code=502,
            detail="Could not generate AI suggestions",
        ) from error


# --------------------------------------------------
# JOB DESCRIPTION (JD) RELEVANCE ENDPOINT (ISOLATED)
# --------------------------------------------------

@app.post("/analyze-jd")
async def analyze_jd(data: dict):
    """Analyze resume relevance against a specific Job Description."""
    resume_text = data.get("resumeText") or data.get("resume_text") or ""
    jd_text = data.get("jdText") or data.get("jd_text") or ""

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is required to calculate JD relevance",
        )

    if not isinstance(jd_text, str) or not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description text is required",
        )

    try:
        result = analyze_jd_relevance(
            resume_text,
            jd_text,
        )
        return result
    except Exception as error:
        logger.exception("JD relevance analysis failed: %s", error)
        raise HTTPException(
            status_code=500,
            detail="Failed to analyze Job Description relevance",
        ) from error
