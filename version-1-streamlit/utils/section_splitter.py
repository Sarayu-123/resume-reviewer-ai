def split_sections(text):
    sections = {"education": "", "skills": "", "projects": "", "experience": ""}

    current_section = None

    for line in text.split("\n"):
        clean_line = line.strip()
        lower_line = clean_line.lower()

        # Education detection
        if any(
            keyword in lower_line
            for keyword in ["education", "academic background", "qualification"]
        ):
            current_section = "education"
            continue

        # Skills detection
        if any(
            keyword in lower_line
            for keyword in ["skills", "technical skills", "core competencies"]
        ):
            current_section = "skills"
            continue

        # Projects detection
        if any(
            keyword in lower_line
            for keyword in ["projects", "academic projects", "personal projects"]
        ):
            current_section = "projects"
            continue

        # Experience detection
        if any(
            keyword in lower_line
            for keyword in ["experience", "work experience", "professional experience"]
        ):
            current_section = "experience"
            continue

        if current_section:
            sections[current_section] += clean_line + "\n"

    return sections
