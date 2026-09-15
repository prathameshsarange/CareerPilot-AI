import hashlib
import json
import os

import streamlit as st

from agents.master_agent import MasterAgent
from pypdf import PdfReader
from schemas.report_schema import ReportSchema


CACHE_DIR = os.path.join("data", ".resume_cache")


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


def _cache_path(resume_text: str) -> str:
    digest = hashlib.sha256(resume_text.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{digest}.json")


def _load_disk_cache(resume_text: str):
    path = _cache_path(resume_text)
    try:
        with open(path, "r", encoding="utf-8") as cache_file:
            return ReportSchema.model_validate(json.load(cache_file))
    except (FileNotFoundError, OSError, ValueError, TypeError):
        return None


def _save_disk_cache(resume_text: str, report: ReportSchema) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _cache_path(resume_text)
    temporary_path = f"{path}.tmp"
    with open(temporary_path, "w", encoding="utf-8") as cache_file:
        json.dump(report.model_dump(mode="json"), cache_file)
    os.replace(temporary_path, path)


def analyze_resume(pdf_path):
    """Returns the structured ReportSchema object (not markdown)."""

    resume_text = extract_text(pdf_path)

    cached_report = _load_disk_cache(resume_text)
    if cached_report is not None:
        return cached_report

    report = _run_pipeline(resume_text)
    _save_disk_cache(resume_text, report)

    return report
