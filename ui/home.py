import os
import io
from datetime import datetime

import streamlit as st

from services.resume_service import analyze_resume
from services.report_service import report_to_markdown
from ui.dataset_page import show_dataset


def show_home():
    st.set_page_config(page_title="DataPilot AI", page_icon="🤖", layout="wide")

    # load local CSS
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'><h2>🤖 DataPilot AI</h2><div class='version'>v1.0</div></div>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Navigation", ["📄 Resume Analyzer", "📊 Dataset Analyzer"])
        st.markdown("---")
        st.markdown("**Features**")
        st.markdown("- Resume Analyzer\n- Dataset Analyzer\n- ML Advisor\n- Reports")
        st.markdown("---")
        st.markdown("<div style='font-size:12px;color:var(--text-light)'>Powered by Gemini AI · Built with Python + Streamlit</div>", unsafe_allow_html=True)

    if page == "📊 Dataset Analyzer":
        show_dataset()
        return

    # HERO
    st.markdown(
        """
<div class="hero">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap">
    <div>
      <h1 style="margin:0">🤖 DataPilot AI</h1>
      <p style="margin:6px 0 0 0;">Premium AI Career Copilot — polish resumes, discover skill gaps, and get a learning roadmap.</p>
      <div style="margin-top:12px"><a class="cta" href="#upload">🚀 Analyze Your Resume</a></div>
    </div>
    <div style="min-width:220px; text-align:right">
      <div style="font-weight:700;font-size:18px">Get recruiter-ready resumes</div>
      <div style="color:var(--text-light)">AI-guided improvements & tailored roadmaps</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Pull previously computed report from session state (if any) for the metric cards
    report = st.session_state.get("report")

    def _truncate(text, max_len=28):
        return text if len(text) <= max_len else text[:max_len - 1].rstrip() + "…"

    col1, col2, col3, col4 = st.columns(4, gap="large")
    col1.metric("ATS Score", f"{report.resume_analysis.ats_score}%" if report else "—")
    col2.metric("Resume Rating", f"{report.resume_analysis.resume_rating}/100" if report else "—")
    col3.metric("Career Domain", _truncate(report.career_domain.domain) if report else "—", help=report.career_domain.domain if report else None)
    col4.metric("Experience Level", report.career_domain.level if report else "—")

    st.markdown("<div id='upload'></div>", unsafe_allow_html=True)

    upload_col, details_col = st.columns([2, 1])

    with upload_col:
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📄 Drag & drop or click to upload (PDF)", type=["pdf"], key="resume_uploader")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getbuffer()
            st.markdown(f"<div class='file-preview'><strong>{uploaded_file.name}</strong> — {len(bytes_data)//1024} KB</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True, disabled=(uploaded_file is None))

    with details_col:
        st.markdown("<h4 style='margin-top:0'>How it works</h4>", unsafe_allow_html=True)
        st.markdown("- Upload a PDF resume.<br>- Click Analyze Resume.<br>- Explore dashboard and download reports.", unsafe_allow_html=True)

    if analyze_btn and uploaded_file is not None:

        save_dir = os.path.join("data", "resumes")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("🤖 AI Analysing your Resume"):
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

    st.success("✅ Analysis completed")
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
            st.markdown("<div class='card'><h3>Resume Score</h3>", unsafe_allow_html=True)
            st.metric("ATS Score", f"{ra.ats_score}%")
            st.metric("Resume Rating", f"{ra.resume_rating}/100")
            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            st.markdown("<div class='card'><h3>Career Domain</h3>", unsafe_allow_html=True)
            st.write(f"**{cd.domain}** ({cd.level}, {cd.confidence}% confidence)")
            st.write(cd.reason)
            st.markdown("</div>", unsafe_allow_html=True)

        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.markdown("<div class='card'><h3>Skill Gap</h3>", unsafe_allow_html=True)
            st.write("**Existing:** " + ", ".join(sg.existing_technical + sg.existing_soft))
            st.write("**Missing:** " + ", ".join(sg.missing_technical + sg.missing_soft))
            st.write("**Priority:** " + ", ".join(sg.priority_skills))
            st.markdown("</div>", unsafe_allow_html=True)

        with g2:
            st.markdown("<div class='card'><h3>Learning Roadmap</h3>", unsafe_allow_html=True)
            st.write("**Day 30:** " + "; ".join(rm.day30))
            st.write("**Day 60:** " + "; ".join(rm.day60))
            st.write("**Day 90:** " + "; ".join(rm.day90))
            st.markdown("</div>", unsafe_allow_html=True)

        r1, r2 = st.columns(2, gap="large")
        with r1:
            st.markdown("<div class='card'><h3>Recommended Certifications</h3>", unsafe_allow_html=True)
            for c in report.certifications:
                st.markdown(f"<div class='cert-card'><strong>{c.name}</strong> — {c.platform} ({c.duration}, {c.difficulty})</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            st.markdown("<div class='card'><h3>Recommended Projects</h3>", unsafe_allow_html=True)
            for p in report.projects:
                st.markdown(f"<div class='cert-card'><strong>{p.name}</strong> [{', '.join(p.tech_stack)}] — {p.difficulty}<br>{p.description}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>Interview Preparation</h3>", unsafe_allow_html=True)
        st.write("**Technical:** " + "; ".join(iv.technical))
        st.write("**HR:** " + "; ".join(iv.hr))
        st.write("**Behavioral:** " + "; ".join(iv.behavioral))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>Career Opportunities</h3>", unsafe_allow_html=True)
        st.write("**Roles:** " + ", ".join(cr.roles))
        st.write(f"**Salary:** {cr.salary}")
        st.write(f"**Future Scope:** {cr.future_scope}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card highlight'><h3>Final Career Advice</h3>", unsafe_allow_html=True)
        st.write(report.final_advice)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("# Full AI Report")
        st.markdown(report_to_markdown(report))

    with tabs[2]:
        st.markdown("### Download Report")
        md_content = report_to_markdown(report)
        st.download_button(
            label="Download Markdown",
            data=md_content,
            file_name="datapilot_report.md",
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
                label="Download PDF",
                data=pdf_buffer,
                file_name="datapilot_report.pdf",
                mime="application/pdf",
            )
        except Exception:
            st.info("PDF generation not available (install reportlab to enable PDF downloads).")

    st.divider()
    st.info("💡 Tip: use the Dashboard tab for a concise overview, Full Report for details.")