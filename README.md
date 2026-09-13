# DataPilot AI

AI career copilot for resume analysis and dataset analysis.

## Live Demo

[Open the live DataPilot AI demo](https://datapilot-ai11212.streamlit.app/)

## Overview

DataPilot AI is a Streamlit application that uses Google Gemini to analyze PDF resumes and CSV datasets. Resume analysis produces structured career guidance, while dataset analysis summarizes data quality and insights and provides machine-learning recommendations.

## Features

- **Resume Analyzer:** Upload a PDF resume to get resume analysis, career-domain classification, skill-gap analysis, a 30/60/90-day roadmap, interview questions, project and certification suggestions, and career guidance.
- **Dataset Analyzer:** Upload a CSV to preview the data, inspect basic dataset information, identify missing values and duplicate rows, and view a generated histogram.
- **ML Advisor:** Get AI-generated suggestions for problem type, algorithms, evaluation metrics, and feature-engineering ideas based on the uploaded dataset.
- **AI-generated reports:** View the resume report in the app and download it as Markdown or PDF.

## Tech Stack

- Python
- Streamlit
- Google Gemini API with structured JSON output
- Pydantic
- pandas
- reportlab

## How It Works

Resume analysis uses a five-agent pipeline. Each stage passes its structured output to the next stage:

```text
ResumeAgent -> SkillGapAgent -> RoadmapAgent -> InterviewAgent -> CareerAdvisorAgent
```

The dataset workflow uses a separate two-agent flow:

```text
DatasetAgent -> MLAdvisorAgent
```

## Screenshots

Add screenshots here when they are available:

![Resume Analyzer screenshot](path/to/resume-screenshot.png)

![Dataset Analyzer screenshot](path/to/dataset-screenshot.png)

## Local Setup

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/prathameshsarange/DataPilot-AI.git
cd DataPilot-AI
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Start the Streamlit app:

```powershell
streamlit run app.py
```

## Project Structure

```text
DataPilot-AI/
├── agents/       # Resume, career, dataset, and ML advisor agents
├── services/     # Resume, dataset, and report services
├── ui/           # Streamlit home and dataset pages
├── schemas/      # Pydantic report schemas
├── core/         # Gemini client, prompts, configuration, and JSON helpers
├── app.py        # Application entry point
└── requirements.txt
```