# 📄 Resume Reviewer AI

> An AI-powered resume analysis system that evaluates resumes, analyzes skills and formatting, matches candidates with target roles, and provides AI-generated improvement suggestions.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![AI](https://img.shields.io/badge/AI-Ollama-purple)
![Frontend](https://img.shields.io/badge/Frontend-Next.js-black)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)

---

## 🧠 About the Project

**Resume Reviewer AI** is a resume analysis project developed through two iterations.

The project started as a **Streamlit-based Python prototype** and was later redesigned into a **full-stack web application using Next.js, React, TypeScript, and FastAPI**.

The system is designed to help analyze a resume from multiple perspectives:

- 📊 Resume scoring
- 🧩 Resume section detection
- 🛠️ Skill analysis
- 🎯 Role-based matching
- 📝 Formatting analysis
- 🤖 AI-powered improvement suggestions
- 📄 PDF and DOCX resume processing

---

# 🔄 Project Evolution

The project consists of two versions.

| | 🧪 Version 1 | 🚀 Version 2 |
|---|---|---|
| Frontend | Streamlit | Next.js + React |
| Language | Python | TypeScript + Python |
| Backend | Streamlit application | FastAPI |
| UI | Streamlit UI | Custom web dashboard |
| AI | Ollama | Ollama |
| Architecture | Prototype | Full-stack |
| API Layer | Integrated | Dedicated API routes + FastAPI |
| Resume Processing | Python | Python |
| Purpose | Initial prototype | Structured full-stack application |

---

# 🧪 Version 1 — Streamlit Prototype

The first version was developed as a Python-based prototype.

### Core capabilities

- 📄 PDF/DOCX resume extraction
- 🔍 Resume section detection
- 📊 Resume scoring
- 🎯 Role matching
- 🛠️ Skill matching
- ⚠️ Formatting analysis
- 🤖 AI-powered bullet suggestions

### Technology

```text
Python
│
├── Streamlit
├── pdfplumber
├── python-docx
├── Requests
└── Ollama
```

👉 **[View Version 1 →](./version-1-streamlit)**

---

# 🚀 Version 2 — Full-Stack Application

Version 2 restructures the original prototype into a full-stack application.

### Frontend

```text
Next.js
   ↓
React
   ↓
TypeScript
   ↓
Custom Dashboard UI
```

### Backend

```text
FastAPI
   ↓
Resume Processing
   ↓
Analysis Agents
   ↓
Skill / Role / Formatting Analysis
   ↓
Ollama
```

### Key improvements

- 🎨 Modern web interface
- ⚛️ React-based frontend
- 🟦 TypeScript
- ⚡ Next.js
- 🐍 FastAPI backend
- 🔌 API-based communication
- 🧩 Modular backend architecture
- 🤖 Local AI processing through Ollama

👉 **[View Version 2 →](./version-2-nextjs-fastapi)**

---

# 🏗️ Overall Architecture

```text
                    📄 Resume
                       │
                       ▼
              ┌─────────────────┐
              │   User Interface │
              └────────┬────────┘
                       │
                       ▼
             ┌────────────────────┐
             │ Resume Processing  │
             └─────────┬──────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     📊 Scoring    🛠️ Skills    🎯 Role Match
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
              🤖 AI Suggestions
                       │
                       ▼
                  📋 Results
```

---

# 📂 Repository Structure

```text
resume-reviewer-ai/
│
├── 📄 README.md
│
├── 🧪 version-1-streamlit/
│   ├── 📄 README.md
│   ├── app.py
│   ├── requirements.txt
│   ├── agents/
│   └── utils/
│
└── 🚀 version-2-nextjs-fastapi/
    ├── 📄 README.md
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

---

# 🎯 Project Goals

The project focuses on building a system that can:

1. 📄 Read and process resumes
2. 🔍 Identify important resume sections
3. 📊 Evaluate resume quality
4. 🛠️ Analyze skills
5. 🎯 Compare skills against target roles
6. ⚠️ Identify formatting-related issues
7. 🤖 Generate AI-powered suggestions
8. 🌐 Present the analysis through a usable interface

---

# 🛠️ Technologies Used

### Version 1

- 🐍 Python
- 🎈 Streamlit
- 📄 pdfplumber
- 📝 python-docx
- 🤖 Ollama
- 🌐 Requests

### Version 2

- ⚡ Next.js
- ⚛️ React
- 🟦 TypeScript
- 🎨 Tailwind CSS
- 🐍 Python
- 🚀 FastAPI
- 🦄 Uvicorn
- 🤖 Ollama
- 📄 pdfplumber
- 📝 python-docx

---

# 🔮 Future Improvements

Possible future improvements include:

- 🔐 User authentication
- 💾 Resume history and storage
- 📈 Resume analytics dashboard
- 📋 Job description upload
- 🔗 Resume-to-JD matching
- 📊 More detailed ATS-oriented analysis
- 📤 Exportable analysis reports
- ☁️ Production deployment
- 🧠 Support for additional local/remote AI models

---

# 👩‍💻 Project

**Resume Reviewer AI**

Built as a progression from a Python/Streamlit prototype to a structured full-stack AI application.

---

⭐ If you find the project useful, consider giving the repository a star.
