# 🚀 Resume Reviewer AI — Version 2

> A full-stack AI-powered resume analysis platform built with Next.js, React, TypeScript, FastAPI, and Ollama.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-blue?logo=typescript)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-black)

---

# 🧠 Overview

**Resume Reviewer AI — Version 2** is the full-stack evolution of the original Streamlit prototype.

Instead of keeping the entire application inside Streamlit, Version 2 separates the system into:

```text
🎨 Frontend
Next.js + React + TypeScript
          │
          ▼
🔌 API Layer
Next.js API Routes
          │
          ▼
⚙️ Backend
FastAPI + Python
          │
          ▼
🧠 Resume Analysis
Agents + Utilities
          │
          ▼
🤖 AI
Ollama
```

This separation makes the application more modular and suitable for further development.

---

# ✨ Features

## 📄 Resume Processing

Upload and process resumes in:

- PDF
- DOCX

The backend extracts resume text and passes it through the analysis pipeline.

---

## 📊 Resume Analysis

The application provides structured resume analysis including:

- Resume scoring
- Section detection
- Formatting analysis
- Skill analysis
- Role matching
- Matched skills
- Missing skills

---

## 🎯 Role Matching

The backend contains role-matching logic for evaluating resume relevance against target roles.

The analysis can identify:

```text
🎯 Target Role
      │
      ▼
Required Skills
      │
      ├───────────────┐
      ▼               ▼
✅ Matched        ❌ Missing
Skills             Skills
```

---

## 🛠️ Skill Matching

The skill-matching component analyzes the skills identified in the resume and compares them with role requirements.

This provides a clearer view of:

### ✅ Skills already present

and

### ❌ Skills that may need to be added or strengthened

---

## ⚠️ Formatting Analysis

The formatting agent performs formatting-related analysis based on the implemented backend logic.

---

## 🤖 AI-Powered Suggestions

The application integrates with **Ollama** for local AI processing.

AI suggestions can be requested through the application's AI suggestion functionality.

The architecture keeps AI processing separate from the UI so the frontend does not need to directly implement the resume-analysis logic.

---

# 🏗️ System Architecture

```text
                         👤 USER
                           │
                           ▼
                ┌─────────────────────┐
                │   Next.js Frontend  │
                │                     │
                │  React + TypeScript │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     API Routes      │
                │                     │
                │ /api/analyze        │
                │ /api/ai-suggestions │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    FastAPI Backend  │
                │                     │
                │     main.py         │
                └──────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        📊 Scoring    🎯 Role Match   🛠️ Skills
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                   ⚠️ Formatting
                           │
                           ▼
                    🤖 Ollama
                           │
                           ▼
                   📋 Analysis Result
                           │
                           ▼
                    🎨 Web Dashboard
```

---

# 🔌 API Flow

The frontend communicates with API endpoints for different operations.

### Resume Analysis

```text
Frontend
   │
   │ Resume
   ▼
/api/analyze
   │
   ▼
FastAPI
   │
   ▼
Resume Processing
   │
   ├── Text Extraction
   ├── Section Detection
   ├── Skill Analysis
   ├── Role Matching
   └── Formatting Analysis
   │
   ▼
Analysis Result
   │
   ▼
Frontend Dashboard
```

### AI Suggestions

```text
Frontend
   │
   ▼
/api/ai-suggestions
   │
   ▼
AI Processing
   │
   ▼
Ollama
   │
   ▼
Generated Suggestions
   │
   ▼
Frontend
```

---

# 🧰 Tech Stack

## 🎨 Frontend

| Technology | Purpose |
|---|---|
| ⚡ Next.js | Web application framework |
| ⚛️ React | UI development |
| 🟦 TypeScript | Type-safe frontend development |
| 🎨 Tailwind CSS | Styling |
| 🧩 UI Components | Reusable interface components |

---

## ⚙️ Backend

| Technology | Purpose |
|---|---|
| 🐍 Python | Backend development |
| 🚀 FastAPI | API framework |
| 🦄 Uvicorn | ASGI server |
| 📄 pdfplumber | PDF processing |
| 📝 python-docx | DOCX processing |

---

## 🤖 AI

| Technology | Purpose |
|---|---|
| 🤖 Ollama | Local AI model execution |

---

# 📂 Project Structure

```text
version-2-nextjs-fastapi/
│
├── 🎨 app/
│   ├── api/
│   │   ├── ai-suggestions/
│   │   │   └── route.ts
│   │   │
│   │   └── analyze/
│   │       └── route.ts
│   │
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
│
├── 🧩 components/
│   ├── dashboard/
│   │   ├── empty-state.tsx
│   │   ├── header.tsx
│   │   ├── resume-upload.tsx
│   │   ├── score-card.tsx
│   │   ├── skill-chart.tsx
│   │   └── suggestions-panel.tsx
│   │
│   └── ui/
│       └── reusable UI components
│
├── ⚙️ backend/
│   ├── agents/
│   │   ├── content_agent.py
│   │   ├── formatting_agent.py
│   │   ├── role_matcher.py
│   │   └── skill_matcher.py
│   │
│   ├── utils/
│   │   ├── docx_reader.py
│   │   ├── llm_extractor.py
│   │   ├── pdf_reader.py
│   │   └── section_splitter.py
│   │
│   └── main.py
│
├── 🪝 hooks/
│   ├── use-mobile.ts
│   └── use-toast.ts
│
├── 📚 lib/
│   ├── types.ts
│   └── utils.ts
│
├── 🖼️ public/
│
├── 🎨 styles/
│
├── package.json
├── package-lock.json
├── next.config.mjs
├── postcss.config.mjs
└── tsconfig.json
```

---

# ⚙️ Local Setup

## 1️⃣ Install Frontend Dependencies

Open a terminal inside:

```text
version-2-nextjs-fastapi
```

Run:

```powershell
npm install
```

---

# 2️⃣ Start the Frontend

Run:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

---

# 3️⃣ Start the Backend

Open a **second terminal**.

Navigate to the backend:

```powershell
cd backend
```

Activate the Python virtual environment:

```powershell
..\venv\Scripts\Activate.ps1
```

Then start FastAPI:

```powershell
python -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

# 🖥️ Running Both Services

You need **two terminals**.

### Terminal 1 — Frontend

```powershell
npm run dev
```

```text
http://localhost:3000
```

### Terminal 2 — Backend

```powershell
cd backend
..\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

```text
http://127.0.0.1:8000
```

---

# 🤖 Ollama Setup

Version 2 can use Ollama for local AI processing.

Make sure Ollama is installed and the required model is available.

Example:

```powershell
ollama pull phi
```

Start Ollama if it is not already running:

```powershell
ollama serve
```

---

# 🔄 Complete Application Flow

```text
                    👤 USER
                      │
                      ▼
                📄 Upload Resume
                      │
                      ▼
             🎨 Next.js Dashboard
                      │
                      ▼
                 🔌 API Route
                      │
                      ▼
                🚀 FastAPI
                      │
                      ▼
              📑 Extract Resume
                      │
                      ▼
              🧩 Split Sections
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     📊 Score      🎯 Role       🛠️ Skills
                   Matching
        │             │             │
        └─────────────┼─────────────┘
                      ▼
               ⚠️ Formatting
                      │
                      ▼
                🤖 Ollama
                      │
                      ▼
             💡 AI Suggestions
                      │
                      ▼
              📋 Final Analysis
                      │
                      ▼
             🎨 Dashboard Results
```

---

# 🔄 What Changed from Version 1?

Version 1:

```text
Streamlit
    │
    ├── UI
    ├── Resume Processing
    ├── Analysis
    └── AI
```

Version 2:

```text
Next.js
   │
   ▼
API Layer
   │
   ▼
FastAPI
   │
   ├── Resume Processing
   ├── Agents
   ├── Skill Matching
   ├── Role Matching
   └── Formatting Analysis
           │
           ▼
        Ollama
```

### Major architectural changes

| Area | Version 1 | Version 2 |
|---|---|---|
| UI | Streamlit | Next.js + React |
| Type System | Python | TypeScript + Python |
| Backend | Streamlit | FastAPI |
| API Architecture | Integrated | Dedicated |
| UI Components | Streamlit | React components |
| Backend Organization | Basic | Agents + utilities |
| Application Structure | Prototype | Full-stack |

---

# 🎯 Design Objective

The goal of Version 2 is not simply to replace Streamlit.

The objective is to move from a prototype architecture toward a more modular application where:

```text
Frontend
    ↓
API
    ↓
Backend
    ↓
Analysis Modules
    ↓
AI
```

Each layer has a more clearly defined responsibility.

---

# 🔮 Future Improvements

Potential extensions include:

- 📋 Job Description upload
- 🎯 Resume ↔ Job Description matching
- 📊 Advanced ATS-oriented analysis
- 💾 Resume history
- 👤 User accounts
- 📈 Analytics dashboard
- 📤 PDF/report export
- ☁️ Cloud deployment
- 🔐 Authentication
- 🧠 Additional AI model support

---

# 🧪 Project Status

**Version:** 2.0

**Architecture:** Full-stack

**Frontend:** Next.js + React + TypeScript

**Backend:** FastAPI + Python

**AI:** Ollama

**Status:** Development / Portfolio Project

---

# 🔗 Related Version

This application evolved from:

👉 **[Version 1 — Streamlit Prototype](../version-1-streamlit)**

👉 **[Back to Project Overview](../)**

---

# 👩‍💻 Author

**N. Ch. Krishna Sri Sarayu**

Computer Science Engineering — Artificial Intelligence & Machine Learning

Sreenidhi Institute of Science and Technology

---

⭐ **If you find this project interesting, consider starring the repository.**
