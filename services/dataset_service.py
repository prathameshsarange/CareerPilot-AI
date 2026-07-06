import time

from google.genai.errors import ServerError

from agents.dataset_agent import DatasetAgent
from agents.ml_advisor_agent import MLAdvisorAgent


def _with_retry(fn, *args):
    delays = [2, 5, 10]
    last_error = None

    for delay in delays:
        try:
            return fn(*args)
        except ServerError as e:
            last_error = e
            time.sleep(delay)

    raise Exception("Gemini server is busy. Please try again in a minute.") from last_error


def analyze_dataset(csv_path):

    dataset = _with_retry(DatasetAgent().analyze, csv_path)
    ml = _with_retry(MLAdvisorAgent().suggest, dataset)

    return dataset, ml