def calculate_skill_matches(text: str, role: str):
    text = text.lower()

    role_skills = {
        "Software Engineer": [
            "python", "java", "c++", "javascript", "react",
            "node", "sql", "docker", "git"
        ],
        "AI/ML Engineer": [
            "python", "pytorch", "tensorflow", "machine learning",
            "deep learning", "nlp", "pandas", "numpy", "scikit-learn"
        ],
        "Data Analyst": [
            "sql", "excel", "power bi", "tableau", "python",
            "statistics", "data analysis", "pandas"
        ]
    }

    # Default to Software Engineer if role not found
    skills = role_skills.get(role, role_skills["Software Engineer"])

    matches = []
    for skill in skills:
        occurrences = text.count(skill)

        if occurrences >= 3:
            score = 90
            found = True
        elif occurrences == 2:
            score = 75
            found = True
        elif occurrences == 1:
            score = 60
            found = True
        else:
            score = 0
            found = False

        matches.append({
            "skill": skill.title(),
            "match": score,
            "found": found
        })

    return matches