import os
import io
from datetime import datetime

import streamlit as st

from services.resume_service import analyze_resume
from services.report_service import report_to_markdown
from ui.dataset_page import show_dataset


BRAND_MARK = """<svg class="mark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2L3 7v10l9 5 9-5V7l-9-5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M12 12l9-5M12 12v10M12 12L3 7" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
</svg>"""

ICON_DOC = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6 2h9l5 5v15H6V2z" stroke="currentColor" stroke-width="1.6"/><path d="M15 2v5h5" stroke="currentColor" stroke-width="1.6"/></svg>"""
ICON_TARGET = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4.5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="1" fill="currentColor"/></svg>"""
ICON_GAP = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 17l5-6 4 4 9-11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
ICON_ROADMAP = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 20l6-16 4 10 6-10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
ICON_CERT = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="9" r="6" stroke="currentColor" stroke-width="1.6"/><path d="M9 14l-2 7 5-3 5 3-2-7" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>"""
ICON_PROJECT = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="4" width="18" height="14" rx="1.5" stroke="currentColor" stroke-width="1.6"/><path d="M3 9h18" stroke="currentColor" stroke-width="1.6"/></svg>"""
ICON_INTERVIEW = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4h16v11H8l-4 4V4z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>"""
ICON_CAREER = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 21V10l9-6 9 6v11" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 21v-7h6v7" stroke="currentColor" stroke-width="1.6"/></svg>"""
ICON_ADVICE = """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 18h6M10 22h4M12 2a6 6 0 0 0-3.5 10.9c.5.4.8 1 .8 1.7V16h5.4v-1.4c0-.7.3-1.3.8-1.7A6 6 0 0 0 12 2z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>"""


def show_home():
    st.set_page_config(page_title="CareerPilot AI", page_icon="◆", layout="wide")

    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(
            f"<div class='sidebar-brand'>{BRAND_MARK}<h2>CareerPilot AI</h2>"
            f"<span class='version'>v1.0</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")
        page = st.radio(
            "Navigation",
            [":material/description: Resume Analyzer", ":material/bar_chart: Dataset Analyzer"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown("**Features**")
        st.markdown("- Resume Analyzer\n- Dataset Analyzer\n- Live Salary Intelligence\n- ML Advisor\n- Reports")
        st.markdown("---")
        st.markdown(
            "<div class='sidebar-footnote'>Powered by Gemini AI<br>Built with Python + Streamlit</div>",
            unsafe_allow_html=True,
        )

    if "Dataset Analyzer" in page:
        show_dataset()
        return

    # HERO
    st.markdown(
        """
<div class="hero">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:2rem;flex-wrap:wrap">
    <div>
    <h1>CareerPilot AI</h1>
    <p class="tagline">AI-Powered Resume &amp; Job Intelligence Platform</p>
      <a class="cta" href="#upload">Analyze your resume →</a>
    </div>
    <div class="side-note">
      <div class="headline">Get recruiter-ready resumes</div>
      <div class="sub">AI-guided improvements &amp; tailored roadmaps</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    report = st.session_state.get("report")

    col1, col2, col3, col4 = st.columns(4, gap="large")
    col1.metric("ATS Score", f"{report.resume_analysis.ats_score}%" if report else "—")
    col2.metric("Resume Rating", f"{report.resume_analysis.resume_rating}/100" if report else "—")
    # No truncation + hover-only tooltip: that pattern is invisible on touch devices.
    # Full value is shown; long labels wrap onto a second line instead of being cut.
    col3.metric("Career Domain", report.career_domain.domain if report else "—")
    col4.metric("Experience Level", report.career_domain.level if report else "—")

    st.markdown("<div id='upload'></div>", unsafe_allow_html=True)

    upload_col, details_col = st.columns([2, 1])

    with upload_col:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            ":material/upload_file: Drag & drop or click to upload (PDF)",
            type=["pdf"],
            key="resume_uploader",
        )
        if uploaded_file is not None:
            bytes_data = uploaded_file.getbuffer()
            st.markdown(
                f"<div class='file-preview'>{uploaded_file.name} — {len(bytes_data)//1024} KB</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        analyze_btn = st.button(
            ":material/rocket_launch: Analyze Resume",
            use_container_width=True,
            disabled=(uploaded_file is None),
        )

    with details_col:
        st.markdown("<h4 style='margin-top:0'>How it works</h4>", unsafe_allow_html=True)
        st.markdown("- Upload a PDF resume.<br>- Click Analyze Resume.<br>- Explore dashboard and download reports.", unsafe_allow_html=True)

    if analyze_btn and uploaded_file is not None:

        save_dir = os.path.join("data", "resumes")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("AI analyzing your resume…"):
            try:
                report = analyze_resume(save_path)
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                return

        st.session_state["report"] = report

        report_md = report_to_markdown(report)
        os.makedirs("reports", exist_ok=True)
        report_path = os.path.join("reports", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)
        st.session_state["report_path"] = report_path

        st.rerun()

    if report is None:
        return

    st.success("Analysis completed", icon=":material/check_circle:")
    tabs = st.tabs(["Dashboard", "Full Report", "Download"])

    ra = report.resume_analysis
    cd = report.career_domain
    sg = report.skill_gap
    rm = report.roadmap
    iv = report.interview
    cr = report.career

    with tabs[0]:

        s1, s2 = st.columns([2, 3], gap="large")
        with s1:
            st.markdown(f"<div class='card'><h3>{ICON_TARGET} Resume Score</h3>", unsafe_allow_html=True)
            st.metric("ATS Score", f"{ra.ats_score}%")
            st.metric("Resume Rating", f"{ra.resume_rating}/100")
            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            st.markdown(f"<div class='card'><h3>{ICON_CAREER} Career Domain</h3>", unsafe_allow_html=True)
            st.write(f"**{cd.domain}** ({cd.level}, {cd.confidence}% confidence)")
            st.write(cd.reason)
            st.markdown("</div>", unsafe_allow_html=True)

        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.markdown(f"<div class='card'><h3>{ICON_GAP} Skill Gap</h3>", unsafe_allow_html=True)
            st.write("**Existing:** " + ", ".join(sg.existing_technical + sg.existing_soft))
            st.write("**Missing:** " + ", ".join(sg.missing_technical + sg.missing_soft))
            st.write("**Priority:** " + ", ".join(sg.priority_skills))
            st.markdown("</div>", unsafe_allow_html=True)

        with g2:
            st.markdown(f"<div class='card'><h3>{ICON_ROADMAP} Learning Roadmap</h3>", unsafe_allow_html=True)
            st.write("**Day 30:** " + "; ".join(rm.day30))
            st.write("**Day 60:** " + "; ".join(rm.day60))
            st.write("**Day 90:** " + "; ".join(rm.day90))
            st.markdown("</div>", unsafe_allow_html=True)

        r1, r2 = st.columns(2, gap="large")
        with r1:
            st.markdown(f"<div class='card'><h3>{ICON_CERT} Recommended Certifications</h3>", unsafe_allow_html=True)
            for c in report.certifications:
                st.markdown(f"<div class='cert-card'><strong>{c.name}</strong> — {c.platform} ({c.duration}, {c.difficulty})</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            st.markdown(f"<div class='card'><h3>{ICON_PROJECT} Recommended Projects</h3>", unsafe_allow_html=True)
            for p in report.projects:
                st.markdown(f"<div class='cert-card'><strong>{p.name}</strong> [{', '.join(p.tech_stack)}] — {p.difficulty}<br>{p.description}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='card'><h3>{ICON_INTERVIEW} Interview Preparation</h3>", unsafe_allow_html=True)
        st.write("**Technical:** " + "; ".join(iv.technical))
        st.write("**HR:** " + "; ".join(iv.hr))
        st.write("**Behavioral:** " + "; ".join(iv.behavioral))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='card'><h3>{ICON_CAREER} Career Opportunities</h3>", unsafe_allow_html=True)
        st.write("**Roles:** " + ", ".join(cr.roles))
        st.write(f"**Future Scope:** {cr.future_scope}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='card highlight'><h3>{ICON_ADVICE} Live Salary Intelligence</h3>", unsafe_allow_html=True)
        st.write(cr.salary)
        st.caption("Salary guidance is enriched with live job-listing data when Adzuna credentials are configured.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='card highlight'><h3>{ICON_ADVICE} Final Career Advice</h3>", unsafe_allow_html=True)
        st.write(report.final_advice)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("# Full AI Report")
        st.markdown(report_to_markdown(report))

    with tabs[2]:
        st.markdown("### Download Report")
        md_content = report_to_markdown(report)
        st.download_button(
            label=":material/download: Download Markdown",
            data=md_content,
            file_name="careerpilot_report.md",
            mime="text/markdown",
        )

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            textobj = c.beginText(40, 750)
            for line in md_content.splitlines():
                textobj.textLine(line[:90])
                if textobj.getY() < 40:
                    c.drawText(textobj)
                    c.showPage()
                    textobj = c.beginText(40, 750)
            c.drawText(textobj)
            c.save()
            pdf_buffer.seek(0)
            st.download_button(
                label=":material/download: Download PDF",
                data=pdf_buffer,
                file_name="careerpilot_report.pdf",
                mime="application/pdf",
            )
        except Exception:
            st.info("PDF generation not available (install reportlab to enable PDF downloads).")

    st.divider()
    st.info("Tip: use the Dashboard tab for a concise overview, Full Report for details.", icon=":material/lightbulb:")
