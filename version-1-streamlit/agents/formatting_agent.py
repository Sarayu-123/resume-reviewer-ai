def check_formatting(sections):
    issues = []
    warnings = []

    # Check missing sections
    for name, content in sections.items():
        if not content.strip():
            issues.append(f"{name.capitalize()} section is missing.")

    # Check very short sections
    for name, content in sections.items():
        if content and len(content.strip()) < 50:
            warnings.append(f"{name.capitalize()} section is very short.")

    return {"issues": issues, "warnings": warnings}
