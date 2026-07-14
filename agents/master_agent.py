import time

from google.genai.errors import ServerError

from agents.resume_agent import ResumeAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import RoadmapAgent
from agents.interview_agent import InterviewAgent
from agents.project_agent import CareerAdvisorAgent
from schemas.report_schema import ReportSchema


def _with_retry(fn, *args):
    """Retry a stage on Gemini server errors with backoff. JSON errors are not retried
    (they indicate a prompt/schema issue, not a transient failure)."""

    delays = [2, 5, 10]
    last_error = None

    for delay in delays:
        try:
            return fn(*args)

        except ServerError as e:
            last_error = e
            time.sleep(delay)

    raise Exception("Gemini server is busy. Please try again later.") from last_error


def _flatten_to_strings(items):
    """Defensive normalization: Gemini sometimes returns roadmap items as objects
    (e.g. {"skill": "...", "description": "..."}) instead of plain strings, even
    when explicitly told not to. Convert anything that isn't already a string
    into a readable string instead of letting schema validation crash the pipeline."""

    flattened = []

    for item in items:
        if isinstance(item, str):
            flattened.append(item)
        elif isinstance(item, dict):
            parts = [str(v) for v in item.values() if v]
            flattened.append(" — ".join(parts) if parts else str(item))
        else:
            flattened.append(str(item))

    return flattened


class MasterAgent:
    """
    Orchestrates the full career-analysis pipeline as a sequence of specialized agents,
    each consuming the previous agent's output:

    ResumeAgent -> SkillGapAgent -> RoadmapAgent -> InterviewAgent -> CareerAdvisorAgent
    """

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.roadmap_agent = RoadmapAgent()
        self.interview_agent = InterviewAgent()
        self.career_advisor_agent = CareerAdvisorAgent()

    def run(self, resume_text: str) -> ReportSchema:

        # Stage 1: Resume Agent -> career_domain + resume_analysis
        stage1 = _with_retry(self.resume_agent.analyze_resume, resume_text)
        career_domain = stage1["career_domain"]
        resume_analysis = stage1["resume_analysis"]

        # Stage 2: Skill Gap Agent -> skill_gap (uses stage 1 output)
        stage2 = _with_retry(self.skill_gap_agent.analyze, stage1)
        skill_gap = stage2["skill_gap"]

        # Stage 3: Roadmap Agent -> roadmap (uses stage 2 output)
        stage3 = _with_retry(self.roadmap_agent.generate, stage2)
        roadmap = stage3["roadmap"]
        roadmap["day30"] = _flatten_to_strings(roadmap.get("day30", []))
        roadmap["day60"] = _flatten_to_strings(roadmap.get("day60", []))
        roadmap["day90"] = _flatten_to_strings(roadmap.get("day90", []))

        # Stage 4: Interview Agent -> interview (uses stage 1 output)
        stage4 = _with_retry(self.interview_agent.generate, stage1)
        interview = stage4["interview"]

        # Stage 5: Career Advisor Agent -> certifications, projects, career, final_advice
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
            raise Exception(f"Pipeline output did not match schema.\n\n{e}")