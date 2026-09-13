import streamlit as st

from agents.master_agent import MasterAgent
from pypdf import PdfReader


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        content = page.extract_text()

        if content:

            text += content + "\n"

    return text


@st.cache_data(show_spinner=False)
def _run_pipeline(resume_text: str):
    """Cached on the extracted resume TEXT, not the file path — so re-uploading
    the same resume (even under a different filename) reuses the previous
    5-call Gemini pipeline result instead of spending 5-15 fresh API calls.
    Cache is process-wide and lives until the app restarts."""

    return MasterAgent().run(resume_text)


def analyze_resume(pdf_path):
    """Returns the structured ReportSchema object (not markdown)."""

    resume_text = extract_text(pdf_path)

    report = _run_pipeline(resume_text)

    return report
