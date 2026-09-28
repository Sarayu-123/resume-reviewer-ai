def check_formatting(sections):

    issues = []
    warnings = []

    for key, value in sections.items():
        if value.strip() == "":
            warnings.append(f"{key} section missing")

    return {
        "issues": issues,
        "warnings": warnings
    }