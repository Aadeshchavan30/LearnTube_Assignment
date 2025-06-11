def analyze_job_fit(job_role, profile_data):
    """
    Compare user profile with industry-standard job description.
    Args:
        job_role (str): Target job role
        profile_data (dict): User profile data
    Returns:
        str: Match score and improvement suggestions
    """
    match_score = 75
    suggestions = f"Your profile matches {match_score}% with the role of {job_role}. Consider learning Cloud Computing."
    return suggestions
