def analyze_profile(profile_data):
    """
    Analyze LinkedIn profile sections for gaps and inconsistencies.
    Args:
        profile_data (dict): Scraped LinkedIn profile data
    Returns:
        str: Analysis summary
        str: Suggested improvements
    """
    # Initialize analysis and gaps strings
    analysis_parts = []
    gaps_parts = []

    # Check About section
    about = profile_data.get("about", "")
    if not about or len(about.strip()) < 50:
        analysis_parts.append("Your About section is missing or too brief.")
        gaps_parts.append("Write a detailed About section (at least 200-300 words) summarizing your professional journey, key skills, and achievements. Include keywords relevant to your industry.")
    else:
        analysis_parts.append("Your About section is present and provides a good overview.")

    # Check Experience section
    experience = profile_data.get("experience", [])
    if not experience or len(experience) < 1:
        analysis_parts.append("Your Experience section is missing or incomplete.")
        gaps_parts.append("Add at least 2-3 recent job roles with detailed descriptions of your responsibilities and achievements. Use action verbs and quantify results where possible.")
    elif len(experience) < 3:
        analysis_parts.append("Your Experience section could be more comprehensive.")
        gaps_parts.append("Consider adding more roles or detailing your contributions in existing roles to showcase a broader range of experience.")
    else:
        analysis_parts.append("Your Experience section is strong with multiple roles listed.")

    # Check Skills section
    skills = profile_data.get("skills", [])
    if not skills or len(skills) < 5:
        analysis_parts.append("Your Skills section lacks detail or is missing.")
        gaps_parts.append("Add at least 5-10 relevant skills to your profile. Include both technical and soft skills specific to your target roles or industry.")
    elif len(skills) < 10:
        analysis_parts.append("Your Skills section could use more entries.")
        gaps_parts.append("Expand your Skills section by adding more niche or advanced skills relevant to your field to stand out.")
    else:
        analysis_parts.append("Your Skills section is well-detailed with a good number of entries.")

    # Check Education section
    education = profile_data.get("education", [])
    if not education or len(education) < 1:
        analysis_parts.append("Your Education section is missing or incomplete.")
        gaps_parts.append("Include your educational background, such as degrees or relevant coursework, to build credibility.")
    else:
        analysis_parts.append("Your Education section is adequately filled.")

    # Check Certifications section
    certifications = profile_data.get("certifications", [])
    if not certifications or len(certifications) < 1:
        analysis_parts.append("Your Certifications section is missing or lacks entries.")
        gaps_parts.append("Consider earning and adding certifications relevant to your field (e.g., online courses from Coursera or LinkedIn Learning) to boost your profile.")
    elif len(certifications) < 3:
        analysis_parts.append("Your Certifications section could be enhanced.")
        gaps_parts.append("Add more certifications to demonstrate continuous learning and expertise in your domain.")
    else:
        analysis_parts.append("Your Certifications section is strong with multiple entries.")

    # Combine analysis and gaps into final strings
    analysis = " ".join(analysis_parts) if analysis_parts else "Your profile lacks sufficient data for a detailed analysis."
    gaps = " ".join(gaps_parts) if gaps_parts else "No specific improvements could be identified due to insufficient profile data."

    return analysis, gaps

def suggest_improvements(profile_data):
    """
    Generate specific improvement suggestions.
    Args:
        profile_data (dict): Profile data
    Returns:
        str: Detailed suggestions
    """
    suggestions = []
    skills = profile_data.get("skills", [])
    about = profile_data.get("about", "")
    experience = profile_data.get("experience", [])
    certifications = profile_data.get("certifications", [])

    if not about or len(about.strip()) < 50:
        suggestions.append("Craft a compelling About section that tells your professional story, highlights your unique value, and includes industry-specific keywords to improve visibility.")
    if len(skills) < 10:
        suggestions.append("Enhance your Skills section by adding relevant technical and soft skills. Research job descriptions in your field to identify high-demand skills to include.")
    if len(experience) < 3:
        suggestions.append("Detail your Experience section with specific achievements and metrics (e.g., 'Increased sales by 20%') to demonstrate impact in your roles.")
    if len(certifications) < 3:
        suggestions.append("Pursue certifications relevant to your career goals (e.g., Google Analytics, AWS Certified Solutions Architect) and list them to show commitment to professional growth.")

    return " ".join(suggestions) if suggestions else "Ensure all sections of your profile are complete to receive tailored improvement suggestions."
