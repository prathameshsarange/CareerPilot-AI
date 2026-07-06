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


def analyze_resume(pdf_path):
    """Returns the structured ReportSchema object (not markdown)."""

    resume_text = extract_text(pdf_path)

    report = MasterAgent().run(resume_text)

    return report