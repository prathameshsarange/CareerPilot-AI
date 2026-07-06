::: {align="center"}
# 🤖 DataPilot AI

### AI-Powered Career Intelligence Platform --- Multi-Agent Pipeline

Analyze resumes • Detect ATS Issues • Find Skill Gaps • Generate Career
Roadmaps • AI Interview Preparation • Dataset Intelligence

```{=html}
<p align="center">
```
`<a href="#">`{=html}`<img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white">`{=html}`</a>`{=html}
`<a href="#">`{=html}`<img src="https://img.shields.io/badge/Google-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white">`{=html}`</a>`{=html}
`<a href="#">`{=html}`<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">`{=html}`</a>`{=html}
`<a href="#">`{=html}`<img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge">`{=html}`</a>`{=html}
`<a href="#">`{=html}`<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">`{=html}`</a>`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<img src="https://img.shields.io/github/stars/prathameshsarange/DataPilot-AI?style=social">`{=html}
`<img src="https://img.shields.io/github/forks/prathameshsarange/DataPilot-AI?style=social">`{=html}
```{=html}
</p>
```
**🔗 Live App:**
https://datapilot-ai-jnzhywdgqgbpenmwchhqg6.streamlit.app/
:::

------------------------------------------------------------------------

## 📖 About This Project

DataPilot AI was built as a capstone project for the **5-Day AI Agents
Intensive: Vibe Coding Course with Google (Kaggle)**.

The project demonstrates a sequential multi-agent workflow using the
Gemini API. Instead of relying on a single LLM response, the application
divides resume analysis into multiple specialized AI agents. Each agent
produces structured output that is validated with Pydantic before being
passed to the next stage, improving reliability and consistency.

The application also includes a Dataset Intelligence module that
analyzes uploaded CSV datasets and recommends suitable machine learning
approaches.

------------------------------------------------------------------------

## 🧠 Multi-Agent Architecture

``` text
                    Resume PDF
                         │
                         ▼
                 PDF Text Extraction
                         │
                         ▼
              Resume Agent
                         │
                         ▼
               Skill Gap Agent
                         │
                         ▼
                Roadmap Agent
                         │
                         ▼
              Interview Agent
                         │
                         ▼
           Career Advisor Agent
                         │
                         ▼
           Pydantic Schema Validation
                         │
                         ▼
          Interactive Streamlit Dashboard
```

Resume analysis uses retry logic with exponential backoff to handle
temporary Gemini API failures.

Dataset analysis follows a lightweight two-agent flow:

``` text
CSV Dataset
     │
     ▼
Dataset Agent
     │
     ▼
ML Advisor Agent
```

------------------------------------------------------------------------

## ✨ Features

### Resume Intelligence

-   ATS Score & Resume Rating
-   Career Domain Detection
-   Skill Gap Analysis
-   30/60/90-Day Learning Roadmap
-   Interview Question Generation
-   Certification Recommendations
-   Project Suggestions
-   Career Guidance
-   Downloadable PDF/Markdown Reports

### Dataset Intelligence

-   CSV Upload
-   Dataset Preview
-   Missing & Duplicate Value Detection
-   Histogram Generation
-   AI Dataset Insights
-   Machine Learning Algorithm Recommendations

------------------------------------------------------------------------

## 🛠️ Technology Stack

  Category        Technologies
  --------------- ------------------------------------------
  Language        Python 3.14
  AI              Google Gemini 2.5 Flash (`google-genai`)
  Frontend        Streamlit
  Validation      Pydantic
  PDF Parsing     PyPDF
  Data Analysis   Pandas
  Visualization   Matplotlib
  Report Export   ReportLab

------------------------------------------------------------------------

## 📂 Project Structure

``` text
DataPilot-AI
│
├── agents/
├── core/
├── schemas/
├── services/
├── ui/
├── utils/
├── app.py
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## 🚀 Setup & Run Locally

``` bash
git clone https://github.com/prathameshsarange/DataPilot-AI.git
cd DataPilot-AI

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

``` env
GEMINI_API_KEY=your_api_key_here
```

Run the application:

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## ☁️ Deployment

The application is deployed on **Streamlit Community Cloud**.

Live Demo: https://datapilot-ai-jnzhywdgqgbpenmwchhqg6.streamlit.app/

The Gemini API key is securely stored using Streamlit Secrets.

-------------------------------------------------------------------------


## 📷 Screenshots

### Resume Analyzer

![Resume Dashboard](assets/resume.png)

### Dataset Analyzer

![Dataset Dashboard](assets/dataset.png)
-------------------------------------------------------------------------

## 🚀 Future Roadmap

-   ✅ Multi-Agent Resume Analysis
-   ✅ Dataset Intelligence
-   ✅ Structured Output Validation
-   ✅ Retry Logic
-   ⏳ Resume vs Job Description Matching
-   ⏳ Function Calling
-   ⏳ Live Job Recommendations
-   ⏳ User Authentication

------------------------------------------------------------------------

## 👨‍💻 Developer

**Prathamesh Sarange**

B.Tech Computer Science Engineering

Sipna College of Engineering and Technology

-   GitHub: https://github.com/prathameshsarange

------------------------------------------------------------------------

::: {align="center"}
Built with **Python, Google Gemini AI, Streamlit, and Pydantic**

Capstone Project for **Google × Kaggle -- 5-Day AI Agents Intensive**
:::
