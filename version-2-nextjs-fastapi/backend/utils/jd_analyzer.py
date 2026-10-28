"""Job Description (JD) analyzer: extracts requirements, calculates relevance score against resume, and provides tailored suggestions.

Completely isolated from the main resume review workflow.
"""

import json
import logging
import os
import re
import requests

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
ENABLE_JD_OLLAMA = os.getenv("ENABLE_JD_OLLAMA", "false").lower() in ("true", "1", "yes")

# Common tech aliases and normalizations
COMMON_TECH_ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "node.js": "node",
    "nodejs": "node",
    "next.js": "next.js",
    "nextjs": "next.js",
    "vue.js": "vue",
    "vuejs": "vue",
    "angular.js": "angular",
    "angularjs": "angular",
    "c++": "c++",
    "c plus plus": "c++",
    "c#": "c#",
    "c sharp": "c#",
    ".net": ".net",
    "dotnet": ".net",
    "golang": "go",
    "scikit-learn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "machine-learning": "machine learning",
    "deep-learning": "deep learning",
    "natural language processing": "nlp",
    "large language models": "llm",
    "large language model": "llm",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "microsoft azure": "azure",
    "power bi": "power bi",
    "powerbi": "power bi",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest apis": "rest api",
    "rest api": "rest api",
    "tailwind css": "tailwind",
    "tailwindcss": "tailwind",
    "ci/cd": "ci/cd",
    "cicd": "ci/cd",
    "continuous integration": "ci/cd",
    "k8s": "kubernetes",
    "fast-api": "fastapi",
    "spring-boot": "spring boot",
}

# Known acronyms for uppercase presentation
ACRONYMS = {
    "aws", "gcp", "sql", "ci/cd", "html", "css", "api", "php", "nlp",
    "llm", "etl", "rest api", "ui", "ux", "qa", "ios", "bi"
}

# Curated catalog of skills across engineering, data, cloud, and product
SKILL_CATALOG = {
    # Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "c", "go",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "dart", "html",
    "css", "sql", "bash", "shell", "powershell", "perl",
    # Frontend / Mobile
    "react", "next.js", "vue", "angular", "svelte", "tailwind", "bootstrap",
    "redux", "zustand", "mobx", "react native", "flutter", "android", "ios",
    "webpack", "vite", "sass", "material ui",
    # Backend / APIs
    "node", "express", "django", "flask", "fastapi", "spring boot", "spring",
    ".net", "graphql", "rest api", "grpc", "microservices", "websocket",
    "fastify", "nestjs", "ruby on rails", "laravel",
    # Databases / Storage
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
    "dynamodb", "sqlite", "oracle", "snowflake", "bigquery", "mariadb",
    # DevOps / Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible",
    "ci/cd", "jenkins", "github actions", "gitlab", "linux", "nginx",
    "prometheus", "grafana", "helm",
    # Data & AI/ML
    "pandas", "numpy", "machine learning", "deep learning", "tensorflow",
    "pytorch", "scikit-learn", "keras", "nlp", "llm", "langchain", "spark",
    "hadoop", "kafka", "rabbitmq", "airflow", "etl", "data pipeline",
    "tableau", "power bi", "looker", "excel", "statistics",
    # Methodologies & Testing
    "git", "agile", "scrum", "jira", "unit testing", "selenium", "cypress",
    "playwright", "jest", "pytest", "figma"
}


def format_skill_display(skill: str) -> str:
    """Format skill name nicely for display (preserving acronyms)."""
    s_lower = skill.lower().strip()
    if s_lower in ACRONYMS:
        return s_lower.upper()
    return skill.title()


def normalize_skill(skill: str) -> str:
    """Normalize skill name using known aliases."""
    cleaned = re.sub(r"\s+", " ", skill.lower().strip())
    return COMMON_TECH_ALIASES.get(cleaned, cleaned)


def extract_skills_from_text(text: str) -> set[str]:
    """Extract known technical skills and qualifications from any text (deterministic)."""
    found = set()
    text_lower = text.lower()

    # Check against known aliases and catalog
    all_check_terms = set(SKILL_CATALOG) | set(COMMON_TECH_ALIASES.keys())
    for term in all_check_terms:
        escaped = re.escape(term)
        if term in ("c++", "c#", ".net"):
            pattern = rf"(?:^|\s|[,;/|()]){escaped}(?:$|\s|[,;/|()])"
        else:
            pattern = rf"(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])"

        if re.search(pattern, text_lower):
            found.add(normalize_skill(term))

    return found


def extract_jd_skills_with_llm(jd_text: str) -> list[str]:
    """Optionally use Ollama to identify specialized JD skills/requirements when enabled."""
    if not ENABLE_JD_OLLAMA:
        return []

    prompt = f"""Extract key technical skills, tools, programming languages, and qualifications required in this Job Description.
Return valid JSON only in this format:
{{"skills": ["skill1", "skill2"]}}

Rules:
- Include ONLY technical tools, technologies, methodologies, and specific job requirements.
- Do NOT include generic soft skills like "good communication", "team player", "leadership".
- Keep skill names concise (1-3 words).

Job Description:
{jd_text[:3000]}
"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=3,
        )
        if response.status_code == 200:
            data = json.loads(response.json().get("response", "{}"))
            skills = data.get("skills", [])
            if isinstance(skills, list):
                return [
                    normalize_skill(s)
                    for s in skills
                    if isinstance(s, str) and 2 <= len(s.strip()) <= 40
                ]
    except Exception as err:
        logger.debug("Ollama JD skill extraction skipped: %s", err)

    return []


def analyze_jd_relevance(resume_text: str, jd_text: str) -> dict:
    """Compare resume text against job description text and compute relevance and suggestions."""
    if not jd_text or not jd_text.strip():
        return {
            "jdScore": 0,
            "matchedSkills": [],
            "missingSkills": [],
            "totalJdSkills": 0,
            "suggestions": [
                {
                    "title": "Empty Job Description",
                    "description": "Please provide a valid Job Description to calculate relevance.",
                    "type": "format",
                }
            ],
        }

    # 1. Extract requirements from JD
    jd_skills = extract_skills_from_text(jd_text)

    # Try LLM extraction if enabled
    if ENABLE_JD_OLLAMA:
        llm_skills = extract_jd_skills_with_llm(jd_text)
        for s in llm_skills:
            jd_skills.add(s)

    # 2. Extract skills from Resume
    resume_skills = extract_skills_from_text(resume_text)
    resume_lower = resume_text.lower()

    matched = []
    missing = []

    for skill in sorted(jd_skills):
        skill_clean = normalize_skill(skill)
        escaped = re.escape(skill_clean)
        if skill_clean in ("c++", "c#", ".net"):
            pattern = rf"(?:^|\s|[,;/|()]){escaped}(?:$|\s|[,;/|()])"
        else:
            pattern = rf"(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])"

        if skill_clean in resume_skills or re.search(pattern, resume_lower):
            matched.append(format_skill_display(skill))
        else:
            missing.append(format_skill_display(skill))

    total_jd_skills = len(matched) + len(missing)

    # 3. Calculate JD Relevance Score (0-100)
    if total_jd_skills > 0:
        jd_score = round((len(matched) * 100) / total_jd_skills)
    else:
        # Fallback if JD text was too generic for skill keywords: check word overlap
        jd_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", jd_text.lower()))
        resume_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", resume_lower))
        overlap = len(jd_words & resume_words)
        total = max(len(jd_words), 1)
        jd_score = min(100, round((overlap * 100) / total))

    # 4. Generate Targeted JD Suggestions
    suggestions = []

    if missing:
        top_missing = missing[:4]
        suggestions.append({
            "title": "Include Missing JD Requirements",
            "description": f"The job description explicitly emphasizes {', '.join(top_missing)}. If you have worked with these technologies or methodologies, add them to your skills list or project bullets.",
            "type": "missing",
        })

    if matched:
        top_matched = matched[:3]
        suggestions.append({
            "title": "Spotlight Matching Strengths",
            "description": f"You match key requirements for {', '.join(top_matched)}. Emphasize these skills in your experience section and quantify results achieved using them.",
            "type": "highlight",
        })

    if jd_score >= 75:
        suggestions.append({
            "title": "High Relevance - Tailor Summary",
            "description": "Your background matches this job description strongly. Align your opening summary or objective to echo the role title and primary keywords from this JD.",
            "type": "format",
        })
    elif jd_score >= 40:
        suggestions.append({
            "title": "Moderate Match - Bridge Gaps",
            "description": "You cover foundational skills, but several role-specific tools are missing. Highlight any adjacent tools, personal projects, or relevant certifications to bridge the gap.",
            "type": "missing",
        })
    else:
        suggestions.append({
            "title": "Low Overlap - Significant Customization Needed",
            "description": "This job description requires several key competencies that were not detected in your resume. Consider customizing your resume projects and keywords to align more closely.",
            "type": "missing",
        })

    return {
        "jdScore": jd_score,
        "matchedSkills": matched,
        "missingSkills": missing,
        "totalJdSkills": total_jd_skills,
        "suggestions": suggestions,
    }
