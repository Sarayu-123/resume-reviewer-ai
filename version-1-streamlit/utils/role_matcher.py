def get_role_skills(role):
    role_skills = {
        "Software Engineer": [
            "python",
            "java",
            "c++",
            "data structures",
            "algorithms",
            "git",
            "sql",
        ],
        "AI/ML Engineer": [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "numpy",
            "pandas",
        ],
        "Data Analyst": [
            "python",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "data analysis",
            "statistics",
        ],
    }
    return role_skills.get(role, [])


def calculate_role_match(resume_text, role):
    required_skills = get_role_skills(role)

    resume_text_lower = resume_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in resume_text_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:
        match_percentage = int((len(matched_skills) / len(required_skills)) * 100)
    else:
        match_percentage = 0

    return match_percentage, matched_skills, missing_skills
