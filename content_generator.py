from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def rewrite_profile_section(section, job_role):
    """
    Rewrite a profile section to align with a specific job role.
    Args:
        section (str): Profile section content (e.g., About)
        job_role (str): Target job role
    Returns:
        str: Rewritten content
    """
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
        prompt = f"Rewrite this LinkedIn section for the job role of {job_role}: {section}"
        rewritten = llm.invoke(prompt).content
        return rewritten
    except Exception as e:
        return f"Rewritten {section} tailored for {job_role} with industry keywords. (Error: {str(e)})"
