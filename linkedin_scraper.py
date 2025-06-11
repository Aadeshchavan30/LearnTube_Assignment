from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables
load_dotenv()

def scrape_linkedin_profile(url):
    """
    Scrape LinkedIn profile data using Apify's LinkedIn Profile Batch Scraper actor (No Cookies Required).
    Args:
        url (str): LinkedIn profile URL
    Returns:
        dict: Profile data including About, Experience, Skills, etc., or error message
    """
    try:
        # Initialize Apify client with API token
        api_token = os.environ.get("APIFY_API_TOKEN", "")
        if not api_token:
            return {"error": "Apify API token is required but not found in environment variables."}
        client = ApifyClient(api_token)

        # Extract username or identifier from the URL
        username = url.split('/')[-1] if url.split('/')[-1] else url.split('/')[-2]
        if not username:
            return {"error": "Invalid LinkedIn URL provided. Unable to extract username."}

        # Define input for the LinkedIn Profile Batch Scraper actor
        run_input = {
            "usernames": [username]  # List of usernames or URLs, limited to one for single profile scraping
        }

        # Run the LinkedIn Profile Batch Scraper actor
        actor_name = "apimaestro/linkedin-profile-batch-scraper-no-cookies-required"
        print(f"Starting Apify actor run for {actor_name} with URL: {url}")
        actor = client.actor(actor_name)
        run = actor.call(run_input=run_input)
        print(f"Actor run started. Run ID: {run['id']}, Status: {run['status']}")

        # Fetch the scraped data from the run's dataset with retries
        dataset_id = run["defaultDatasetId"]
        max_retries = 10
        retry_delay = 30  # seconds to wait between retries
        items = []
        for attempt in range(max_retries):
            items = client.dataset(dataset_id).list_items().items
            if items:
                print(f"Data found on attempt {attempt + 1}/{max_retries}.")
                break  # Data found, exit retry loop
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}: No data yet. Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)

        if not items:
            return {"error": "No data found for the provided LinkedIn URL after multiple attempts."}

        # Extract relevant profile data from the first item (since we're scraping one profile)
        raw_profile = items[0] if isinstance(items, list) and items else items
        if not raw_profile:
            return {"error": "No profile data returned from scraper."}

        # Map the raw data to the expected structure for the app
        # Based on the provided JSON output structure from apimaestro/linkedin-profile-batch-scraper-no-cookies-required
        basic_info = raw_profile.get("basic_info", {})
        profile_data = {
            "fullName": basic_info.get("fullname", ""),
            "headline": basic_info.get("headline", ""),
            "about": basic_info.get("about", ""),
            "experience": raw_profile.get("experience", []),
            "skills": [],  # Skills are nested in experience, will extract below
            "education": raw_profile.get("education", []),
            "certifications": []  # Certifications may not be directly available, default to empty list
        }

        # Extract skills from experience entries if available
        all_skills = []
        for exp in profile_data["experience"]:
            if "skills" in exp:
                all_skills.extend(exp.get("skills", []))
        # Deduplicate skills
        profile_data["skills"] = list(set(all_skills)) if all_skills else []

        print("Processed Profile Data for App:", json.dumps(profile_data, indent=2))
        return profile_data

    except Exception as e:
        error_msg = f"Failed to scrape profile: {str(e)}"
        print(error_msg)
        return {"error": error_msg}
