# 📄 Resume Reviewer AI

### From Resume Upload to Actionable Career Insights

An AI-assisted resume analysis system that evaluates resume quality, identifies skill gaps, analyzes formatting, compares skills against target roles, and generates improvement suggestions using Ollama.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
</p>

---

## 🧠 About the Project

Resume Reviewer AI was developed through two iterations: a Python-based Streamlit prototype and a full-stack web application built with Next.js, React, TypeScript, and FastAPI.

Both versions use Ollama for AI-assisted suggestions. Version 2 reorganizes the application architecture and presents analysis results through a more customizable dashboard.

### 🎯 Core Capabilities

- 📄 PDF and DOCX resume text extraction
- 🔍 Resume section detection
- 📊 Resume scoring
- 🧩 Skill matching and gap identification
- 🎯 Role-specific resume analysis
- 📋 Formatting and ATS-readability checks
- 🎓 Education matching and experience detection
- 🤖 Ollama-powered improvement suggestions
- 📈 Structured presentation of analysis results

## 🔄 Project Evolution: Version 1 → Version 2

The project evolved in two dimensions: **application architecture** and **the presentation and interpretation of resume analysis**.

### 🏗️ Architectural Improvements

| Area | Version 1 — Streamlit | Version 2 — Next.js + FastAPI |
|---|---|---|
| Interface | Streamlit components | Custom React dashboard |
| Frontend | Python-based UI | Next.js, React, TypeScript |
| Backend | Integrated Streamlit application | Dedicated FastAPI backend |
| Communication | Integrated application workflow | HTTP API communication |
| Organization | Prototype-oriented structure | More modular frontend and backend |
| AI runtime | Ollama | Ollama |
| Document processing | Python utilities | Python utilities |

**Result:** A clearer separation between the user interface and backend processing, with greater flexibility for frontend customization and independent development.

### 🧠 Analysis & Intelligence Evolution

| Area | Project evolution |
|---|---|
| Resume evaluation | Version 2 presents analysis results in a more structured dashboard. |
| Skill-gap analysis | Results can be presented as matched skills, missing skills, and required-skill coverage. |
| Role-specific feedback | Analysis results are organized around the selected target role. |
| ATS readability | Structural checks are presented separately from other resume-analysis results. |
| Education and experience | Detected information can be shown as separate analysis categories. |
| AI recommendations | Ollama-generated suggestions are presented alongside resume-analysis results. |

**Important distinction:** These comparisons describe the documented project capabilities and Version 2's current output. They do not establish that the underlying AI model became more accurate. Ollama was already present in Version 1.

### 🚀 Potential Next-Level Improvements

The following are future enhancements, not claims of completed functionality:

- **Semantic skill matching:** Recognize relevant synonyms and equivalent terminology.
- **Context-aware recommendations:** Include the selected role and detected skill gaps in AI prompts.
- **Evidence-linked feedback:** Connect recommendations to specific resume content.
- **Job-description comparison:** Compare resume content directly against a supplied job description.
- **More robust AI handling:** Validate model responses and handle unavailable models and timeouts.

---

## 🧪 Version 1 — Streamlit Prototype

A Python-based implementation that established the core resume-analysis workflow.

### Features

- PDF/DOCX text extraction
- Resume section detection
- Resume scoring
- Role and skill matching
- Formatting analysis
- AI-assisted bullet-point suggestions

### Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| pdfplumber | PDF text extraction |
| python-docx | DOCX processing |
| Requests | HTTP communication with Ollama |
| Ollama | Local AI inference |

**Explore:** [Version 1 — Streamlit](./version-1-streamlit/README.md)

---

## 🚀 Version 2 — Full-Stack Application

A redesigned application that separates the frontend from the backend and presents resume-analysis results through a custom web interface.

### Frontend

- **Next.js** — React application framework
- **React** — Component-based interface
- **TypeScript** — Static type checking
- **Tailwind CSS** — UI styling

### Backend and AI

- **Python** — Resume-processing and analysis logic
- **FastAPI** — HTTP API endpoints
- **Uvicorn** — ASGI server
- **pdfplumber** — PDF extraction
- **python-docx** — DOCX processing
- **Ollama** — Local language-model inference

### Analysis Workflow

```text
Resume Upload + Target Role
            │
            ▼
     Document Extraction
            │
            ▼
      Resume Text
            │
            ▼
   Resume Analysis Pipeline
            │
     ┌──────┼─────────┐
     ▼      ▼         ▼
   Skills  Scoring  Readability
     │      │         │
     └──────┼─────────┘
            ▼
   Ollama AI Suggestions
            │
            ▼
    Results Dashboard
```

### Current Analysis Output

Depending on the resume and selected role, Version 2 can display:

- Overall resume score
- Required-skill coverage percentage
- Matched and missing skills
- Individual skill-match results
- ATS-readability estimate based on structural checks
- Education-match information
- Professional-experience detection
- AI-generated improvement suggestions

**Interpretation note:** A skill marked missing may not have been detected by the analyzer; it does not necessarily prove the candidate lacks that skill. Likewise, the ATS-readability estimate is not a guarantee of compatibility with every ATS.

**Explore:** [Version 2 — Next.js + FastAPI](./version-2-nextjs-fastapi/README.md)

---

## 🏗️ Overall System Architecture

```text
                     USER
                      │
                      ▼
              Resume Upload
                      │
                      ▼
              Frontend Interface
                      │
                 HTTP Requests
                      │
                      ▼
               FastAPI Backend
                      │
                      ▼
           Resume Processing Layer
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Skill Match   Scoring    Formatting
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
                Ollama Model
                      │
                      ▼
              AI Suggestions
                      │
                      ▼
              Results Dashboard
```

## 📂 Repository Structure

```text
resume-reviewer-ai/
│
├── README.md
│
├── version-1-streamlit/
│   ├── README.md
│   ├── app.py
│   ├── requirements.txt
│   ├── agents/
│   └── utils/
│
└── version-2-nextjs-fastapi/
    ├── README.md
    ├── app/
    ├── backend/
    ├── components/
    ├── hooks/
    ├── lib/
    ├── public/
    ├── styles/
    ├── package.json
    └── tsconfig.json
```

*This tree summarizes the documented layout. Consult each version's README for its actual entry points and setup instructions.*

## 🛠️ Getting Started

### Prerequisites

- Python
- Node.js and npm for Version 2
- Git
- Ollama and the model configured by the selected version

### Clone the Repository

```bash
git clone https://github.com/Sarayu-123/resume-reviewer-ai.git
cd resume-reviewer-ai
```

### Run Version 1

Follow the setup instructions in [`version-1-streamlit/README.md`](./version-1-streamlit/README.md).

### Run Version 2

Follow the setup instructions in [`version-2-nextjs-fastapi/README.md`](./version-2-nextjs-fastapi/README.md).

The two versions have different dependencies and startup procedures. Refer to their individual READMEs rather than assuming they share the same commands.

## 🔐 Privacy, Accuracy & Limitations

- Ollama can run inference locally when configured to use a local model instance.
- Confirm application network and storage behavior before assuming all resume data remains on your device.
- Analysis quality depends on text extraction, matching rules, role requirements, and model output.
- AI-generated suggestions should be reviewed before applying them.
- Resume scores and ATS-readability estimates are indicators, not guarantees of interview selection or employment.

## 🔮 Future Scope

- Semantic skill matching
- Direct job-description matching
- More context-aware AI recommendations
- Evidence-linked feedback
- Expanded resume analytics
- Exportable analysis reports
- Additional local language models
- Automated testing and more robust error handling

## 👩‍💻 Author

**N Ch Krishna Sri Sarayu**

- [GitHub Profile](https://github.com/Sarayu-123)
- [Project Repository](https://github.com/Sarayu-123/resume-reviewer-ai)

---

<p align="center">
  <b>Analyze better. Identify gaps. Improve with purpose.</b>
</p>
