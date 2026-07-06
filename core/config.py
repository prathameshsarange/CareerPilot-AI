import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_gemini_api_key():
    """
    Return Gemini API key.
    Works both locally (.env) and on Streamlit Cloud (Secrets).
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to .env locally or Streamlit Secrets."
        )

    return api_key