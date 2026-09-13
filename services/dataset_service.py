import hashlib
import time

import streamlit as st
from google.genai.errors import ServerError

from agents.dataset_agent import DatasetAgent
from agents.ml_advisor_agent import MLAdvisorAgent


def _with_retry(fn, *args):
    # Cut from 3 attempts to 2 — a single flaky stage used to cost up to 3
    # calls; a whole resume pipeline could burn 15 calls on transient errors.
    delays = [2, 5]
    last_error = None

    for delay in delays:
        try:
            return fn(*args)
        except ServerError as e:
            last_error = e
            time.sleep(delay)

    raise Exception("Gemini server is busy. Please try again in a minute.") from last_error


def _file_hash(csv_path):
    with open(csv_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


@st.cache_data(show_spinner=False)
def _run_analysis(_csv_path, file_hash):
    """Cached on the file's content hash, not its path — re-analyzing the
    same CSV (even re-uploaded under a different name) skips both Gemini
    calls instead of repeating them. _csv_path is prefixed with underscore
    so Streamlit doesn't try to hash it; file_hash is the real cache key."""

    dataset = _with_retry(DatasetAgent().analyze, _csv_path)
    ml = _with_retry(MLAdvisorAgent().suggest, dataset)

    return dataset, ml


def analyze_dataset(csv_path):

    return _run_analysis(csv_path, _file_hash(csv_path))
