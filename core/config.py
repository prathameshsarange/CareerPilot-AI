import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_gemini_api_key() -> str:
    """Return the configured Gemini API key or raise a user-facing error."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to a .env file or set it "
            "in your environment before running AI analysis."
        )

    return api_key
