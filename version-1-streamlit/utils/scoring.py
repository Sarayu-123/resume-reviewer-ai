def calculate_score(format_result):
    score = 100

    # Deduct 20 points per critical issue
    score -= len(format_result["issues"]) * 20

    # Deduct 10 points per warning
    score -= len(format_result["warnings"]) * 10

    # Prevent negative score
    if score < 0:
        score = 0

    return score
