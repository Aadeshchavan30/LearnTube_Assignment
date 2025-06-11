
**An AI-Powered LinkedIn Profile Optimizer and Career Guidance System**

App url - https://learntubeassignment-ubhb6e93gbqqljkggyxmej.streamlit.app/

## Overview

An interactive AI-powered web application designed to help users optimize their LinkedIn profiles, analyze job fit for target roles, and receive personalized career guidance. Built with Streamlit, LangGraph, and Google Generative AI, the app processes LinkedIn profile data scraped via Apify, provides detailed feedback, suggests improvements, and maintains chat history for a seamless user experience.

### Key Features
- **Interactive Chat Interface**: Users input a LinkedIn profile URL and engage in a chat with an AI assistant for feedback and career advice.
- **Profile Optimization**: Analyzes LinkedIn sections (About, Experience, Skills, etc.) to identify gaps and provide actionable suggestions.
- **Job Fit Analysis**: Compares user profiles with industry-standard job descriptions to generate match scores and improvement tips.
- **Content Enhancement**: Rewrites LinkedIn profile sections to align with specific job roles using GenAI.
- **Career Guidance**: Offers skill gap analysis and learning resource recommendations for target career paths.
- **Memory System**: Retains user context and chat history across sessions using LangGraph's memory capabilities.

## Motivation

This project addresses the need for personalized career development tools by leveraging AI to analyze and enhance LinkedIn profiles, a critical asset in professional networking and job hunting. It aims to empower users to stand out in competitive job markets by providing tailored feedback and actionable career advice through an intuitive chat-based interface.

## Installation and Setup

Follow these instructions to set up and run the app locally.

### Prerequisites
- **Python**: Version 3.9 to 3.13
- **Virtual Environment Manager**: `venv` (recommended, comes with Python)
- **Package Manager**: `pip` (comes with Python)
- **Code Editor**: VS Code or any preferred editor

### Step 1: Clone the Repository

git clone https://github.com/Aadeshchavan30/LearnTube_Assignment 

cd LearnTube_Assignment


### Step 2: Create and Activate a Virtual Environment

Windows (Command Prompt)
python -m venv .venv
.venv\Scripts\activate.bat

Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

macOS/Linux
python -m venv .venv
source .venv/bin/activate


### Step 3: Install Dependencies

pip install -r requirements.txt


### Step 4: Set Up Environment Variables
Create a `.env` file in the project root directory with the following variables:

APIFY_API_TOKEN=[Your Apify API Token]

LINKEDIN_COOKIES=[Your LinkedIn Cookies JSON, if required]

GOOGLE_API_KEY=[Your Gemini API Key for Generative AI]


- Obtain an Apify API token from the Apify platform (free credits available).
- LinkedIn cookies are optional but may be required for some scrapers; format as a JSON list.
- Get a Google API key for accessing the Gemini model via Google Generative AI.

### Step 5: Run the Streamlit App

streamlit run app.py 

- If the above command doesn't work, use:

python -m streamlit run app.py

- The app will open in your default browser at `http://localhost:8501`.

### Step 6: Deactivate the Environment (When Done)

deactivate

## Usage

1. **Access the App**: Open the hosted app at https://learntubeassignment-ubhb6e93gbqqljkggyxmej.streamlit.app/ or run it locally as described in the setup instructions.
2. **Enter LinkedIn URL**: Input a LinkedIn profile URL in the provided text field and click "Analyze Profile" to scrape and analyze the data.
3. **Review Analysis**: View the AI-generated profile analysis and suggested improvements displayed on the app.
4. **Engage in Chat**: Use the chat interface to ask specific questions (e.g., "What skills should I add for a data science role?") for personalized career guidance.
5. **Switch Profile**: Enter a new LinkedIn URL to analyze a different profile; chat history is maintained per profile for context retention.

## Technical Architecture

The app is built using a multi-agent system with LangGraph and LangChain, leveraging Google Generative AI (Gemini 2.0 Flash) for natural language processing tasks. Key components include:

- **Streamlit UI**: Provides an interactive web interface for user input and chat-based feedback.
- **Apify LinkedIn Scraper**: Extracts profile data using the `apimaestro/linkedin-profile-batch-scraper-no-cookies-required` actor.
- **LangGraph Agent System**: Manages profile analysis, job fit scoring, and content rewriting with memory persistence using `MemorySaver` for context retention.
- **GenAI Integration**: Powers detailed profile feedback, career advice, and content enhancement through tailored prompts.

## Challenges and Solutions

- **Challenge: Inconsistent LinkedIn Data**: Free Apify scrapers sometimes returned empty or inconsistent JSON data, often requiring cookies.
  - **Solution**: Used the `apimaestro/linkedin-profile-batch-scraper-no-cookies-required` actor for reliability; implemented retry logic in the scraper to handle delays in data retrieval.
- **Challenge: Chat History Management**: Ensuring chat history isolation per LinkedIn profile to avoid context mixing.
  - **Solution**: Implemented a dictionary-based storage (`chat_history_all`) in Streamlit session state, keyed by profile URL, to maintain separate histories.
- **Challenge: GenAI Response Quality**: Ensuring AI responses are detailed and job-role specific.
  - **Solution**: Crafted detailed prompts with structured data summaries and used error handling to manage API failures gracefully.


## Dependencies

All required packages are listed in `requirements.txt`. Key dependencies include:
- `streamlit`: For the web app interface.
- `apify-client`: For LinkedIn data scraping.
- `langchain-google-genai`, `langchain`, `langgraph`: For AI model integration and multi-agent system.
- `python-dotenv`: For environment variable management.

