
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.8-flash"

client = genai.Client(api_key=API_KEY) if API_KEY else None

# Remember quota failures during this Python process
quota_exhausted = False


def summarize_article(title, description):
    """Generate a concise AI summary with friendly error handling."""

    global quota_exhausted

    if not API_KEY or client is None:
        return (
            "AI summaries are unavailable because the Gemini API key "
            "is missing. Please check your .env file."
        )

    if quota_exhausted:
        return (
            "Gemini's request quota was exhausted earlier. "
            "Please try again after your quota resets."
        )

    if not description or not description.strip():
        description = "No article description is available."

    prompt = f"""
You are a factual news summarization assistant.

Summarize the following news information in 2-3 simple sentences.
Use only the information provided. Do not invent facts.
Return only the summary.

Headline: {title}
Article description: {description}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "Gemini did not return a summary. Please try again."

    except Exception as error:
        error_message = str(error)
        error_upper = error_message.upper()

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_upper:
            quota_exhausted = True
            return (
                "AI summary temporarily unavailable because the "
                "Gemini API quota has been reached. Your news digest "
                "is still working. Please try again after the quota resets."
            )

        if "401" in error_message or "UNAUTHENTICATED" in error_upper:
            return (
                "Gemini authentication failed. Check your API key "
                "and API access settings."
            )

        if "403" in error_message or "PERMISSION_DENIED" in error_upper:
            return (
                "Gemini access was denied. Check your API permissions "
                "and account settings."
            )

        return (
            "Could not generate the AI summary because of a connection "
            "or API error. Please try again later."
        )
