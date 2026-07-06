from pydantic import BaseModel
from typing import List


class CareerDomain(BaseModel):
    domain: str
    confidence: float
    level: str
    reason: str


class ResumeAnalysis(BaseModel):
    ats_score: float
    resume_rating: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]


class SkillGap(BaseModel):
    existing_technical: List[str]
    existing_soft: List[str]
    missing_technical: List[str]
    missing_soft: List[str]
    priority_skills: List[str]


class Roadmap(BaseModel):
    day30: List[str]
    day60: List[str]
    day90: List[str]


class Certification(BaseModel):
    name: str
    platform: str
    duration: str
    difficulty: str


class Project(BaseModel):
    name: str
    tech_stack: List[str]
    difficulty: str
    description: str


class Interview(BaseModel):
    technical: List[str]
    hr: List[str]
    behavioral: List[str]


class Career(BaseModel):
    roles: List[str]
    salary: str
    future_scope: str


class ReportSchema(BaseModel):
    career_domain: CareerDomain
    resume_analysis: ResumeAnalysis
    skill_gap: SkillGap
    roadmap: Roadmap
    certifications: List[Certification]
    projects: List[Project]
    interview: Interview
    career: Career
    final_advice: str