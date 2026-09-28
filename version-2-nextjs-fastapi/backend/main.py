from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from utils.pdf_reader import read_pdf
from utils.docx_reader import read_docx
from utils.llm_extractor import extract_with_llm

import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROLE SKILLS
# -----------------------------
ROLE_SKILLS = {
    "Frontend Developer": ["html","css","javascript","react","next.js","tailwind"],
    "Backend Developer": ["python","java","node","sql","api","django","flask"],
    "Fullstack Developer": ["react","node","python","sql","api","javascript"],
    "Data Scientist": ["python","pandas","numpy","machine learning","statistics"],
    "Machine Learning Engineer": ["python","tensorflow","pytorch","deep learning"],
    "Data Engineer": ["sql","etl","spark","hadoop","pipeline"],
    "Data Analyst": ["sql","excel","power bi","tableau","python"],
    "DevOps Engineer": ["docker","kubernetes","aws","ci/cd","linux"],
    "Cloud Engineer": ["aws","azure","gcp","cloud","terraform"],
    "Mobile Developer": ["android","ios","flutter","react native"],
    "AI Engineer": ["python","nlp","llm","machine learning"],
    "Software Engineer": ["python","java","c++","sql","git"],
    "Product Manager": ["roadmap","agile","scrum","stakeholder"],
    "UX Designer": ["figma","wireframe","ux","ui"],
    "Security Engineer": ["security","network","encryption"],
    "QA Engineer": ["testing","selenium","automation"],
}

ALL_SKILLS = list(set([s for skills in ROLE_SKILLS.values() for s in skills]))

# -----------------------------
# KEYWORD EXTRACTION (STRICT)
# -----------------------------
def extract_keywords(text):
    text = text.lower()
    found = set()

    for skill in ALL_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found.add(skill)

    return found

# -----------------------------
# HYBRID MATCHING
# -----------------------------
def match_skills(text, role):

    role_skills = ROLE_SKILLS.get(role, [])

    # 1. strict keyword extraction
    keyword_skills = extract_keywords(text)

    # 2. LLM extraction
    llm_data = extract_with_llm(text)
    llm_skills = [s.lower() for s in llm_data.get("skills", [])]

    # 3. combine both
    combined_skills = set(keyword_skills) | set(llm_skills)

    matches = []
    matched_count = 0

    for rs in role_skills:

        found = any(rs in s or s in rs for s in combined_skills)

        if found:
            score = 90
            matched_count += 1
        else:
            score = 0

        matches.append({
            "skill": rs.title(),
            "match": score,
            "found": found
        })

    total = len(role_skills) or 1
    role_score = int((matched_count / total) * 100)

    found_kw = [rs for rs in role_skills if rs in combined_skills]
    missing_kw = [rs for rs in role_skills if rs not in combined_skills]

    ats_score = int((len(found_kw) / total) * 100)

    return matches, role_score, found_kw, missing_kw, ats_score, llm_data


# -----------------------------
# ROUTES
# -----------------------------
@app.get("/")
def home():
    return {"message": "Hybrid AI backend running"}


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), role: str = Form(...)):

    # read resume
    if file.filename.endswith(".pdf"):
        text = read_pdf(file.file)
    else:
        text = read_docx(file.file)

    text_lower = text.lower()

    skill_matches, role_score, found_kw, missing_kw, ats_score, llm_data = match_skills(text_lower, role)

    overall_score = int((role_score * 0.7) + (ats_score * 0.3))

    # safe education formatting
    edu = llm_data.get("education", "")

    if isinstance(edu, dict):
        degree_text = f"{edu.get('degree','')} ({edu.get('institution','')})"
    else:
        degree_text = str(edu)

    return {
        "overallScore": overall_score,
        "role": role,
        "fileName": file.filename,

        "experience": {
            "years": llm_data.get("experience_years", 0),
            "relevance": role_score
        },

        "education": {
            "degree": degree_text,
            "match": 75
        },

        "keywords": {
            "found": len(found_kw),
            "missing": len(missing_kw)
        },

        "atsScore": ats_score,
        "skillMatches": skill_matches
    }


@app.post("/ai-suggestions")
async def ai_suggestions(data: dict):

    role = data.get("role", "")
    skills = data.get("skillMatches", [])

    missing = [s["skill"] for s in skills if not s["found"]]
    weak = [s["skill"] for s in skills if s["found"] and s["match"] < 80]

    suggestions = []

    if missing:
        suggestions.append({
            "title": "Add Missing Skills",
            "description": f"For {role}, add: {', '.join(missing[:5])}"
        })

    if weak:
        suggestions.append({
            "title": "Improve Skills",
            "description": f"Strengthen: {', '.join(weak[:5])}"
        })

    if not suggestions:
        suggestions.append({
            "title": "Strong Resume",
            "description": f"Your resume is well aligned for {role}"
        })

    return {"suggestions": suggestions}