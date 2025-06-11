import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from linkedin_scraper import scrape_linkedin_profile
from job_fit_analyzer import analyze_job_fit
from content_generator import rewrite_profile_section
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Initialize session state for memory and user data
if "profile_data" not in st.session_state:
    st.session_state.profile_data = None
if "chat_history_all" not in st.session_state:
    st.session_state.chat_history_all = {}  # Dictionary to store chat history per profile URL
if "current_url" not in st.session_state:
    st.session_state.current_url = None
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "default_thread"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_response" not in st.session_state:
    st.session_state.analysis_response = None  # To store profile analysis
if "improvement_response" not in st.session_state:
    st.session_state.improvement_response = None  # To store suggested improvements

# Streamlit UI Setup
st.title("LearnTube by CareerNinja")
st.subheader("Optimize Your LinkedIn Profile and Career Path")

# Input for LinkedIn Profile URL with a unique key
linkedin_url = st.text_input("Enter your LinkedIn Profile URL:", value="", key="linkedin_url_input")

# Button to trigger profile analysis
if st.button("Analyze Profile") and linkedin_url:
    # Check if the URL is different from the currently analyzed one
    if st.session_state.current_url != linkedin_url:
        # If a new profile URL, update current_url and thread_id
        st.session_state.current_url = linkedin_url
        st.session_state.thread_id = f"thread_{linkedin_url[-10:]}"  # Unique thread ID per profile
        # Initialize chat history for this URL if not already present
        if linkedin_url not in st.session_state.chat_history_all:
            st.session_state.chat_history_all[linkedin_url] = []
        # Clear messages for LLM to start fresh for new profile
        st.session_state.messages = []
        # Clear previous analysis results to avoid displaying old data
        st.session_state.analysis_response = None
        st.session_state.improvement_response = None
        st.write("Starting fresh for a new profile analysis.")
    
    with st.spinner("Scraping and analyzing your profile..."):
        profile_data = scrape_linkedin_profile(linkedin_url)
        st.session_state.profile_data = profile_data
        if "error" in profile_data:
            st.error(profile_data["error"])
        else:
            # Removed display of JSON data on Streamlit app; only log to console for debugging
            print("Debug: Processed Profile Data Passed to LLM:", json.dumps(profile_data, indent=2))  # Print to console for debugging
            
            # Initialize Gemini LLM for analysis
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
            # Initialize memory with a checkpointer
            memory_saver = MemorySaver()
            # Create the agent with a checkpointer for memory
            agent = create_react_agent(
                llm,
                tools=[analyze_job_fit, rewrite_profile_section],
                checkpointer=memory_saver
            )
            # Configure thread ID for memory persistence (unique per profile)
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            # Format input for profile analysis using LLM with detailed prompt
            system_prompt = """You are a professional career coach specializing in LinkedIn profile optimization. Your task is to analyze the provided LinkedIn profile data and provide a detailed, personalized evaluation. Focus on the following sections:
            - fullName: The user's full name.
            - headline: The professional title or tagline.
            - about: The summary section.
            - experience: List of work experiences.
            - skills: List of skills.
            - education: List of educational background entries.
            - certifications: List of certifications.
            For each section:
            - Assess the completeness and quality of the content.
            - Highlight strengths and identify weaknesses or gaps.
            - Provide specific feedback based on the actual data provided.
            Do not give generic responses. Tailor your analysis to the specific details in the data. If a section is empty or lacks detail, note it and explain the impact. Use a structured format with headings for each section analyzed."""
            # Extract key sections for clarity in prompt
            profile_summary = f"""
            Full Name: {profile_data.get('fullName', 'Not provided')}
            Headline: {profile_data.get('headline', 'Not provided')}
            About/Summary: {profile_data.get('about', 'Not provided')}
            Experiences: {json.dumps(profile_data.get('experience', []), indent=2)}
            Skills: {json.dumps(profile_data.get('skills', []), indent=2)}
            Education: {json.dumps(profile_data.get('education', []), indent=2)}
            Certifications: {json.dumps(profile_data.get('certifications', []), indent=2)}
            """
            analysis_input = f"Analyze this LinkedIn profile data in detail:\n{profile_summary}"
            full_input_messages = [
                HumanMessage(content=f"System: {system_prompt}\n{analysis_input}")
            ]
            # Invoke the agent for profile analysis
            result = agent.invoke({"messages": full_input_messages}, config=config)
            # Extract response based on result type
            if isinstance(result, AIMessage):
                analysis_response = result.content
            elif isinstance(result, dict) and "messages" in result:
                last_message = result["messages"][-1] if result["messages"] else {"content": "Sorry, I couldn't analyze your profile."}
                analysis_response = last_message.get("content", "Sorry, I couldn't analyze your profile.") if isinstance(last_message, dict) else last_message.content
            else:
                analysis_response = "Sorry, I couldn't analyze your profile."
            st.session_state.analysis_response = analysis_response  # Store in session state to persist
            
            # Format input for suggested improvements using LLM with detailed prompt
            improvement_prompt = """Based on the LinkedIn profile analysis, provide specific, actionable suggestions for improvement to enhance the profile's effectiveness for job opportunities and career growth. Focus on each section (fullName, headline, about, experience, skills, education, certifications) and suggest:
            - Specific content to add or improve.
            - Keywords or skills to include based on the user's current data.
            - Strategies to align the profile with industry standards.
            Use a structured format with headings for each section. Tailor suggestions to the user's existing data and career context inferred from the profile."""
            full_input_messages.append(HumanMessage(content=improvement_prompt))
            # Invoke the agent for improvement suggestions
            result = agent.invoke({"messages": full_input_messages}, config=config)
            # Extract response based on result type
            if isinstance(result, AIMessage):
                improvement_response = result.content
            elif isinstance(result, dict) and "messages" in result:
                last_message = result["messages"][-1] if result["messages"] else {"content": "Sorry, I couldn't provide suggestions."}
                improvement_response = last_message.get("content", "Sorry, I couldn't provide suggestions.") if isinstance(last_message, dict) else last_message.content
            else:
                improvement_response = "Sorry, I couldn't provide suggestions."
            st.session_state.improvement_response = improvement_response  # Store in session state to persist
            
            # Display results
            st.write("### Profile Analysis")
            st.write(analysis_response)
            st.write("### Suggested Improvements")
            st.write(improvement_response)
            # Update chat history for the current profile with initial bot message
            st.session_state.chat_history_all[linkedin_url].append(("Bot", "Profile analyzed. Here is the detailed feedback and suggestions. Ask me for specific career guidance or profile feedback based on this analysis."))
            st.session_state.messages.append(AIMessage(content="Profile analyzed. Here is the detailed feedback:\n\n**Profile Analysis:**\n" + analysis_response + "\n\n**Suggested Improvements:**\n" + improvement_response + "\n\nAsk me for specific career guidance or profile feedback based on this analysis."))

# Always display the analysis results if they exist for the current profile
if st.session_state.analysis_response and st.session_state.current_url == linkedin_url:
    st.write("### Profile Analysis")
    st.write(st.session_state.analysis_response)
    st.write("### Suggested Improvements")
    st.write(st.session_state.improvement_response)

# Chat Interface for Career Guidance and Profile Feedback
st.write("### Ask for Career Guidance or Profile Feedback")
user_input = st.text_input("Type your question here (e.g., 'What skills should I add for a data science role?' or 'How can I improve my headline?'):", value="", key="user_input_text")
if user_input and st.button("Send"):
    if st.session_state.current_url:
        st.session_state.chat_history_all[st.session_state.current_url].append(("You", user_input))
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Processing your request..."):
            # Initialize Gemini LLM
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
            # Initialize memory with a checkpointer
            memory_saver = MemorySaver()
            # Create the agent with a checkpointer for memory
            agent = create_react_agent(
                llm,
                tools=[analyze_job_fit, rewrite_profile_section],
                checkpointer=memory_saver
            )
            # Configure thread ID for memory persistence (unique per profile)
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            # Format input as messages for Gemini API with profile context
            system_prompt = """You are a professional career coach specializing in LinkedIn profile optimization and career guidance. Use the provided LinkedIn profile data to answer user questions with personalized advice. Tailor your responses to the user's specific background, skills, experiences, and career context. If the user asks about specific career paths, job roles, or profile improvements, provide detailed, actionable suggestions. If no profile data is available, inform the user and suggest analyzing a LinkedIn profile first. Maintain a supportive and professional tone, and retain context from previous interactions."""
            # Check if profile_data exists before accessing it
            if st.session_state.profile_data and "error" not in st.session_state.profile_data:
                profile_summary = f"""
                Full Name: {st.session_state.profile_data.get('fullName', 'Not provided')}
                Headline: {st.session_state.profile_data.get('headline', 'Not provided')}
                About/Summary: {st.session_state.profile_data.get('about', 'Not provided')}
                Experiences: {json.dumps(st.session_state.profile_data.get('experience', []), indent=2)}
                Skills: {json.dumps(st.session_state.profile_data.get('skills', []), indent=2)}
                Education: {json.dumps(st.session_state.profile_data.get('education', []), indent=2)}
                Certifications: {json.dumps(st.session_state.profile_data.get('certifications', []), indent=2)}
                """
            else:
                profile_summary = "No LinkedIn profile data available. Please analyze a profile first by entering a LinkedIn URL and clicking 'Analyze Profile'."
            full_input_messages = [
                HumanMessage(content=f"System: {system_prompt}\nProfile Data Summary for Context:\n{profile_summary}"),
                *st.session_state.messages
            ]
            # Directly invoke the agent with the formatted messages
            result = agent.invoke({"messages": full_input_messages}, config=config)
            # Extract response based on result type
            if isinstance(result, AIMessage):
                response = result.content
            elif isinstance(result, dict) and "messages" in result:
                last_message = result["messages"][-1] if result["messages"] else {"content": "Sorry, I couldn't process your request."}
                response = last_message.get("content", "Sorry, I couldn't process your request.") if isinstance(last_message, dict) else last_message.content
            else:
                response = "Sorry, I couldn't process your request."
            st.session_state.chat_history_all[st.session_state.current_url].append(("Bot", response))
            st.session_state.messages.append(AIMessage(content=response))
    else:
        st.warning("Please analyze a LinkedIn profile first before asking questions.")

# Display Chat History for the Current Profile Only
st.write("### Chat History")
if st.session_state.current_url and st.session_state.current_url in st.session_state.chat_history_all:
    for sender, message in st.session_state.chat_history_all[st.session_state.current_url]:
        st.write(f"**{sender}:** {message}")
else:
    st.write("No chat history available. Analyze a profile and start asking questions!")
