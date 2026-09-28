def calculate_role_match(text, role):

    role_skills = {
        "Software Engineer": ["python", "java", "react"],
        "AI/ML Engineer": ["python", "machine learning", "tensorflow"],
        "Data Analyst": ["sql", "excel", "tableau"]
    }

    text_lower = text.lower()
    skills = role_skills.get(role, [])

    matched = [s for s in skills if s in text_lower]
    missing = [s for s in skills if s not in text_lower]

    match_percentage = int(len(matched) / len(skills) * 100) if skills else 0

    return match_percentage, matched, missing