# ✦ Resume Reviewer AI

### Your resume. Your target role. A clearer path forward.

An AI-powered resume analyzer that evaluates role-specific skill coverage, estimates ATS readability, and generates personalized improvement suggestions using a local LLM.

<p align="center">

  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />

</p>

---

## ✨ Features

| Feature | What it does |
|---|---|
| 📄 Resume Analysis | Extracts and analyzes resume content from supported PDF and DOCX files |
| 🎯 Role-Based Matching | Evaluates skills against the selected job role |
| 📊 Resume Scoring | Displays an application-generated resume score |
| 🧩 Skill Gap Analysis | Highlights detected and missing required skills |
| 🎓 Education Matching | Displays detected education information and its role match |
| 📋 ATS Readability | Checks common resume structure and readability indicators |
| 🤖 AI Suggestions | Generates recommendations to improve role alignment |
| 🖥️ Local LLM | Integrates with Ollama and the configured Phi-3 model |

## ⚙️ Tech Stack

**Frontend:** Next.js · React · TypeScript · Tailwind CSS  
**Backend:** Python · FastAPI · Uvicorn  
**AI:** Ollama · Phi-3  
**Document Processing:** PDF and DOCX extraction utilities  
**Tools:** Git · GitHub · npm

## 🏗️ Architecture

```text
User
 │
 ▼
Next.js + TypeScript
 │  HTTP API requests
 ▼
FastAPI Backend
 ├── Resume Text Extraction
 ├── Role-Based Skill Matching
 ├── Resume & ATS Scoring
 └── AI Suggestion Generation
      │
      ├── PDF / DOCX Processing
      └── Ollama + Phi-3
 │
 ▼
Analysis Dashboard
```

## 🚀 Quick Start

### Prerequisites

[Node.js](https://nodejs.org/) · [Python](https://www.python.org/) · [Ollama](https://ollama.com/)

### 1. Clone

```bash
git clone https://github.com/Sarayu-123/resume-reviewer-ai.git
cd resume-reviewer-ai/version-2-nextjs-fastapi
```

### 2. Start the AI model

```bash
ollama pull phi3
```

Ensure Ollama is running and accessible at `http://localhost:11434`.

### 3. Start the backend

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

Install dependencies and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API documentation: [localhost:8000/docs](http://127.0.0.1:8000/docs)

### 4. Start the frontend

Open a second terminal in `version-2-nextjs-fastapi`:

```bash
npm install
npm run dev
```

Open [localhost:3000](http://localhost:3000).

> Keep the backend and Ollama running while using the application. These commands assume the dependency files and entry points match the paths above.

## 🔍 How It Works

**Upload → Select Role → Analyze → Review → Improve**

1. Upload a supported resume.
2. Select your target job role.
3. Review the resume score, education information, skill matches, and missing skills.
4. Generate AI suggestions and use them to guide improvements.

## 📈 Understanding the Scores

- **Resume Score:** An application-generated assessment based on the implemented scoring logic.
- **Required-Skill Coverage:** The percentage of configured required skills detected in the extracted resume text.
- **ATS Readability Estimate:** A heuristic based on common resume structure and readability checks—not a score from a real ATS.
- **AI Suggestions:** Model-generated recommendations that should be reviewed before applying them.

A missing skill means it was not detected by the analyzer; it does not always prove the skill is absent from the resume.

## 🔐 Privacy & Limitations

- Ollama provides local model inference when configured to use the local instance.
- Verify all application network requests and storage behavior before assuming resume data stays entirely local.
- Results depend on text extraction, role requirements, skill-matching logic, and model output.
- Scores are estimates, not guarantees of ATS success, interview selection, or employment.

## 📁 Project Structure

```text
version-2-nextjs-fastapi/
├── app/                   # Next.js routes
├── components/            # UI components
├── public/                # Static assets
├── main.py                # FastAPI application
├── pdf_reader.py          # PDF extraction
├── docx_reader.py         # DOCX extraction
├── llm_extractor.py       # LLM-assisted extraction
├── package.json           # Frontend dependencies
├── requirements.txt       # Backend dependencies
└── README.md
```

*Adjust the tree to reflect the files actually present in your repository.*

## 🛣️ Future Scope

- Improved skill synonym recognition
- More robust document extraction and validation
- Custom job descriptions and skill requirements
- Expanded automated tests
- Optional analysis export

## 👩‍💻 Author

**N Ch Krishna Sri Sarayu**

[GitHub Profile](https://github.com/Sarayu-123) · [Project Repository](https://github.com/Sarayu-123/resume-reviewer-ai)

---

<p align="center">
  <b>Built to make resume feedback clearer, more actionable, and role-specific.</b>
</p>
