from google import genai

from core.config import get_gemini_api_key

_client = None


def get_gemini_client():
    """Create the Gemini client lazily so the app can load before AI calls."""
    global _client

    if _client is None:
        _client = genai.Client(api_key=get_gemini_api_key())

    return _client
