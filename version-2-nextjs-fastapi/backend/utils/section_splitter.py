def split_sections(text):

    sections = {
        "education": "",
        "experience": "",
        "projects": "",
        "skills": ""
    }

    current = None

    for line in text.split("\n"):

        lower = line.lower()

        if "education" in lower:
            current = "education"

        elif "experience" in lower:
            current = "experience"

        elif "project" in lower:
            current = "projects"

        elif "skill" in lower:
            current = "skills"

        if current:
            sections[current] += line + "\n"

    return sections