import time

from google.genai.errors import ServerError

from agents.interview_agent import InterviewAgent
from agents.project_agent import CareerAdvisorAgent
from agents.resume_agent import ResumeAgent
from agents.roadmap_agent import RoadmapAgent
from agents.skill_gap_agent import SkillGapAgent
from schemas.report_schema import ReportSchema


def _with_retry(fn, *args):
    """Retry a stage on transient Gemini server errors with backoff."""
    delays = [0, 2, 5, 10]
    last_error = None

    for delay in delays:
        try:
            if delay:
                time.sleep(delay)

            return fn(*args)

        except ServerError as e:
            last_error = e

    raise RuntimeError("Gemini server is busy. Please try again later.") from last_error


class MasterAgent:
    """
    Orchestrates the career-analysis pipeline:

    ResumeAgent -> SkillGapAgent -> RoadmapAgent -> InterviewAgent -> CareerAdvisorAgent
    """

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.roadmap_agent = RoadmapAgent()
        self.interview_agent = InterviewAgent()
        self.career_advisor_agent = CareerAdvisorAgent()

    def run(self, resume_text: str) -> ReportSchema:
        if not resume_text or not resume_text.strip():
            raise ValueError("No readable resume text was found in the uploaded PDF.")

        stage1 = _with_retry(self.resume_agent.analyze_resume, resume_text)
        career_domain = stage1["career_domain"]
        resume_analysis = stage1["resume_analysis"]

        stage2 = _with_retry(self.skill_gap_agent.analyze, stage1)
        skill_gap = stage2["skill_gap"]

        stage3 = _with_retry(self.roadmap_agent.generate, stage2)
        roadmap = stage3["roadmap"]

        stage4 = _with_retry(self.interview_agent.generate, stage1)
        interview = stage4["interview"]

        stage5 = _with_retry(self.career_advisor_agent.advise, career_domain, skill_gap)

        report_dict = {
            "career_domain": career_domain,
            "resume_analysis": resume_analysis,
            "skill_gap": skill_gap,
            "roadmap": roadmap,
            "certifications": stage5["certifications"],
            "projects": stage5["projects"],
            "interview": interview,
            "career": stage5["career"],
            "final_advice": stage5["final_advice"],
        }

        try:
            return ReportSchema.model_validate(report_dict)

        except Exception as e:
            raise ValueError(f"Pipeline output did not match schema: {e}") from e
