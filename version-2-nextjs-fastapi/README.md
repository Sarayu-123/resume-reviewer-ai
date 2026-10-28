# 🧠 Resume Reviewer AI

### Analyze your resume. Identify skill gaps. Improve with actionable feedback.

An AI-assisted resume analysis application that evaluates role-specific skill coverage, estimates ATS readability, compares resume relevance directly against target Job Descriptions, and generates improvement suggestions using Ollama.

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
</p>

---

## ✨ Features

- 📄 **Resume Parsing** — Extract text from supported PDF and DOCX files.
- 🎯 **Role-Based Analysis** — Evaluate resume skills against a selected job role.
- 🎯 **Job Description (JD) Match (Optional)** — Compare resume relevance against a specific Job Description, calculate match percentage, identify matched & missing JD keywords, and receive tailored recommendations to bridge gaps.
- 📊 **Resume Scoring** — Display an application-generated resume score.
- 🧩 **Skill-Gap Analysis** — Identify matched and missing required skills.
- 📈 **Skill Coverage** — View required-skill coverage and individual skill-match percentages.
- 🎓 **Education Matching** — Display detected education information and role-match results.
- 💼 **Experience Detection** — Report detected professional experience when available.
- 📋 **ATS Readability Estimate** — Check common resume sections and structural indicators.
- 🤖 **AI Suggestions** — Generate resume-improvement recommendations using Ollama.
- 🖥️ **Interactive Dashboard** — Review analysis results through organized UI components.

## 🧰 Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Package Manager | npm |
| Backend | Python, FastAPI, Uvicorn |
| AI Runtime | Ollama |
| Language Model | Phi-3 (`phi3`) |
| Document Processing | PDF and DOCX extraction utilities |
| Version Control | Git, GitHub |

## 🏗️ Architecture

```text
                        USER
                          │
                          ▼
              Next.js + React + TypeScript
                          │
                     HTTP Requests
                          ▼
                    FastAPI Backend
                          │
                 Python Analysis Layer
         ┌───────────────┼───────────────┬──────────────────┐
         ▼               ▼               ▼                  ▼
      Document         Skill         Scoring &       Job Description (JD)
     Extraction      Matching       Readability           Matching
         │               │               │                  │
         └───────────────┼───────────────┘                  │
                         ▼                                  ▼
                   Ollama / Phi-3                    Relevance & Tailored
                         │                               Suggestions
                         ▼                                  │
                  AI Suggestions                            │
                         │                                  │
                         └─────────────────┬────────────────┘
                                           ▼
                                   Results Dashboard
```

## 🔄 Version 1 → Version 2

Resume Reviewer AI evolved from a Streamlit prototype into a full-stack application with a more customizable interface and more detailed presentation of analysis results.

### 🏗️ Architectural Improvements

| Version 1 — Streamlit | Version 2 — Next.js + FastAPI |
|---|---|
| Python-based Streamlit interface | Next.js, React, and TypeScript frontend |
| UI and analysis workflow closely integrated | Frontend and backend separated through HTTP APIs |
| Streamlit components for displaying results | Custom, reusable dashboard components |
| Python application execution | Dedicated FastAPI backend served by Uvicorn |
| Prototype-oriented structure | More modular frontend and backend organization with isolated feature modules |

**Impact:** Independent frontend and backend development, a customizable interface, and clearer separation of responsibilities.

### 🧠 Intelligence & Analysis Improvements

| Capability | Version 1 | Version 2 |
|---|---|---|
| Resume evaluation | Overall scoring and analysis checks | Separately displays resume score, skill coverage, and ATS readability |
| Skill-gap analysis | Identifies matched and missing skills | Quantifies required-skill coverage and displays individual skill-match percentages |
| Experience reporting | Depends on extracted resume information | Can distinguish undetected experience from a confirmed value |
| Job Description matching | Not supported | Direct comparison against custom Job Descriptions with relevance scoring, matched/missing requirements, and targeted suggestions |
| AI recommendations | Ollama-assisted suggestions | Suggestions presented alongside role-specific analysis and skill gaps |
| Feedback interpretation | Initial resume-review results | More detailed breakdown of skills, education, readability, and recommendations |

**Impact:** More granular and interpretable feedback helps users identify skill gaps and prioritize potential improvements.

### 🚀 Further Intelligence Improvements

These are planned enhancements unless already implemented and tested:

- **Context-aware suggestions:** Include the selected role, detected skills, missing skills, and relevant resume evidence in the Ollama prompt.
- **Semantic skill matching:** Recognize synonyms and equivalent terminology instead of relying only on exact keywords.
- **Evidence-linked recommendations:** Explain which analysis finding supports each suggestion.
- **Validated AI output:** Handle malformed responses, unavailable models, and request timeouts reliably.

*Ollama was already used in Version 1. The project should not claim that AI was newly introduced or that model accuracy improved without evidence.*

## 🚀 Getting Started

### Prerequisites

Install:

- [Node.js and npm](https://nodejs.org/)
- [Python](https://www.python.org/)
- [Ollama](https://ollama.com/)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Sarayu-123/resume-reviewer-ai.git
cd resume-reviewer-ai/version-2-nextjs-fastapi
```

### 2. Start the AI model

```bash
ollama pull phi3
```

Ensure Ollama is running and the configured model is available at `http://localhost:11434`.

### 3. Set up the backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Set up the frontend

Open a second terminal in `version-2-nextjs-fastapi`:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

**Why npm?** `npm install` installs the frontend dependencies defined in `package.json`; `npm run dev` executes the configured Next.js development script. Backend dependencies are installed separately with Python's `pip`.

Keep the backend and Ollama running while using the application. The commands assume the dependency files and entry points are located as described.

## 🔍 How It Works

1. **Upload:** Select a supported resume file (`.pdf` or `.docx`).
2. **Choose a role:** Select the target job role.
3. **Extract:** Convert the document into readable text.
4. **Analyze:** Evaluate skills, education, experience, and readability indicators.
5. **Job Description Match (Optional):** Paste a specific job description to compute a direct relevance score, inspect matched/missing requirements, and receive targeted tailoring tips.
6. **Review:** Inspect the resume score, detected skills, and missing skills.
7. **Improve:** Generate AI suggestions and review potential next steps.

## 📊 Understanding the Results

| Metric | Meaning |
|---|---|
| Resume Score | An application-generated score based on the implemented scoring rules |
| Required-Skill Coverage | Percentage of configured required skills detected in the extracted resume text |
| Skill Match | Individual match results for configured skills |
| JD Relevance Score | Match percentage comparing resume skills against requirements in the provided Job Description |
| ATS Readability Estimate | A heuristic based on structural and readability checks |
| AI Suggestions | Model-generated recommendations that require user review |

**Important:** A missing skill means it was not detected by the analyzer; it does not necessarily prove the skill is absent from the resume. The ATS readability estimate is not a score from a real applicant tracking system and does not guarantee selection.

## 🔐 Privacy & Limitations

- Ollama supports local model inference when configured to use a local instance.
- Verify network requests and storage behavior before assuming all resume data stays local.
- Results depend on document extraction, configured role requirements, matching rules, and model output.
- AI recommendations can be incomplete or inaccurate; verify them before editing your resume.
- Scores are estimates, not guarantees of ATS success, interviews, or employment.
- Never commit private resumes, credentials, or environment files to GitHub.

## 📁 Project Structure

```text
resume-reviewer-ai/
├── version-1-streamlit/
│   └── ...                  # Streamlit implementation
├── version-2-nextjs-fastapi/
│   ├── app/                 # Next.js routes & API handlers
│   ├── components/          # UI components (Dashboard, ScoreCard, JD Cards)
│   ├── public/              # Static assets
│   ├── backend/             # FastAPI backend
│   │   ├── utils/           # Extractors & isolated JD analyzer
│   │   └── main.py          # FastAPI application & endpoints
│   ├── package.json         # Frontend dependencies
│   ├── requirements.txt     # Backend dependencies
│   └── README.md
├── README.md
└── .gitignore
```

## 🛣️ Future Scope

- Semantic skill matching and synonym recognition
- Evidence-linked AI recommendations
- More robust document validation and automated tests
- Exportable analysis reports
- Optional authentication and resume history

## 👩‍💻 Author

**N Ch Krishna Sri Sarayu**

- [GitHub Profile](https://github.com/Sarayu-123)
- [Project Repository](https://github.com/Sarayu-123/resume-reviewer-ai)

---

<p align="center">
  <b>Turning resume analysis into measurable, actionable feedback.</b>
</p>
