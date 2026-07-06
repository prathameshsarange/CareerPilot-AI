import os
from datetime import datetime

from schemas.report_schema import ReportSchema


def report_to_markdown(report: ReportSchema) -> str:
    """Convert the structured pipeline output into a readable Markdown report."""
    cd = report.career_domain
    ra = report.resume_analysis
    sg = report.skill_gap
    rm = report.roadmap
    iv = report.interview
    cr = report.career

    lines = [
        "# DataPilot AI Resume Report",
        "",
        "## Career Domain",
        f"**Domain:** {cd.domain}  ",
        f"**Confidence:** {cd.confidence}%  ",
        f"**Level:** {cd.level}",
        "",
        cd.reason,
        "",
        "## Resume Analysis",
        f"**ATS Score:** {ra.ats_score}%  ",
        f"**Resume Rating:** {ra.resume_rating}/100",
        "",
        "**Strengths:**",
        *_bullet_lines(ra.strengths),
        "",
        "**Weaknesses:**",
        *_bullet_lines(ra.weaknesses),
        "",
        "**Suggestions:**",
        *_bullet_lines(ra.suggestions),
        "",
        "## Skill Gap",
        f"**Existing Technical Skills:** {_join_or_default(sg.existing_technical)}",
        f"**Existing Soft Skills:** {_join_or_default(sg.existing_soft)}",
        f"**Missing Technical Skills:** {_join_or_default(sg.missing_technical)}",
        f"**Missing Soft Skills:** {_join_or_default(sg.missing_soft)}",
        f"**Priority Skills:** {_join_or_default(sg.priority_skills)}",
        "",
        "## Learning Roadmap",
        "**Day 30:**",
        *_bullet_lines(rm.day30),
        "",
        "**Day 60:**",
        *_bullet_lines(rm.day60),
        "",
        "**Day 90:**",
        *_bullet_lines(rm.day90),
        "",
        "## Recommended Certifications",
        *_certification_lines(report),
        "",
        "## Recommended Projects",
        *_project_lines(report),
        "",
        "## Interview Preparation",
        "**Technical:**",
        *_bullet_lines(iv.technical),
        "",
        "**HR:**",
        *_bullet_lines(iv.hr),
        "",
        "**Behavioral:**",
        *_bullet_lines(iv.behavioral),
        "",
        "## Career Opportunities",
        f"**Roles:** {_join_or_default(cr.roles)}",
        f"**Expected Salary:** {cr.salary}",
        f"**Future Scope:** {cr.future_scope}",
        "",
        "## Final Career Advice",
        report.final_advice,
    ]

    return "\n".join(lines)


def save_report(report: str) -> str:
    os.makedirs("reports", exist_ok=True)

    filename = os.path.join(
        "reports",
        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    return filename


def _bullet_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- Not specified."]

    return [f"- {item}" for item in items]


def _join_or_default(items: list[str]) -> str:
    if not items:
        return "Not specified."

    return ", ".join(items)


def _certification_lines(report: ReportSchema) -> list[str]:
    if not report.certifications:
        return ["- Not specified."]

    return [
        f"- **{cert.name}** ({cert.platform}, {cert.duration}, {cert.difficulty})"
        for cert in report.certifications
    ]


def _project_lines(report: ReportSchema) -> list[str]:
    if not report.projects:
        return ["- Not specified."]

    return [
        f"- **{project.name}** [{', '.join(project.tech_stack)}] - "
        f"{project.difficulty}\n  {project.description}"
        for project in report.projects
    ]
