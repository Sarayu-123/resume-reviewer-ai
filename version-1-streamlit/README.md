# 🧪 Resume Reviewer AI — Version 1

> The original Streamlit-based prototype for AI-powered resume analysis.

---

## 📌 Overview

**Version 1** is the initial implementation of Resume Reviewer AI.

It was built using **Python and Streamlit** and focuses on the core resume-analysis pipeline:

```text
📄 Upload Resume
       ↓
📑 Extract Text
       ↓
🔍 Detect Sections
       ↓
📊 Analyze Resume
       ↓
🎯 Match Target Role
       ↓
🛠️ Analyze Skills
       ↓
📈 Calculate Score
       ↓
🤖 Generate Suggestions
```

---

# ✨ Features

### 📄 Resume Upload

Supports resume files in:

- PDF
- DOCX

---

### 🔍 Resume Text Extraction

The application extracts text from uploaded resumes using:

- `pdfplumber` for PDF files
- `python-docx` for DOCX files

---

### 🧩 Section Detection

The resume is processed to identify major sections such as:

```text
👤 Contact / Header
🎓 Education
💼 Experience
🛠️ Skills
🚀 Projects
📜 Certifications
```

---

### 📊 Resume Scoring

The application analyzes the resume and calculates a score based on the implemented resume-analysis logic.

---

### 🎯 Role Matching

The system supports role-oriented analysis.

The resume can be evaluated against target roles such as:

- Software Engineer
- AI/ML Engineer
- Data Analyst

The role matcher identifies relevant skills and missing skills based on the implemented role definitions.

---

### 🛠️ Skill Analysis

The system analyzes the skills present in the resume and compares them with the selected role.

```text
Resume Skills
     │
     ▼
Role Requirements
     │
     ├── ✅ Matched Skills
     │
     └── ❌ Missing Skills
```

---

### ⚠️ Formatting Analysis

The formatting agent checks the resume for formatting-related issues based on the implemented rules.

---

### 🤖 AI Suggestions

The prototype can use **Ollama** for local AI-powered suggestions.

The AI functionality is intended to help improve resume content, including bullet-point wording.

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core application |
| 🎈 Streamlit | User interface |
| 📄 pdfplumber | PDF text extraction |
| 📝 python-docx | DOCX text extraction |
| 🌐 Requests | Communication with local AI service |
| 🤖 Ollama | Local AI processing |

---

# 📂 Project Structure

```text
version-1-streamlit/
│
├── 📄 app.py
├── 📄 requirements.txt
│
├── 🤖 agents/
│   ├── content_agent.py
│   └── formatting_agent.py
│
└── 🧰 utils/
    ├── docx_reader.py
    ├── pdf_reader.py
    ├── role_matcher.py
    ├── scoring.py
    └── section_splitter.py
```

---

# 🔄 Application Flow

```text
                    📄 Resume
                       │
                       ▼
               📤 Streamlit Upload
                       │
                       ▼
              📑 Document Reader
                /            \
               ▼              ▼
            PDF Reader     DOCX Reader
                \            /
                 ▼          ▼
                📝 Extracted Text
                       │
                       ▼
                🧩 Section Splitter
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       📊 Scoring   🎯 Role      ⚠️ Formatting
                   Matching
          │            │            │
          └────────────┼────────────┘
                       ▼
                🤖 AI Suggestions
                       │
                       ▼
                 📋 Final Results
```

---

# ⚙️ Installation

### 1️⃣ Create a virtual environment

From inside this folder:

```powershell
python -m venv .venv
```

### 2️⃣ Activate the environment

```powershell
.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```powershell
streamlit run app.py
```

Streamlit will provide a local URL in the terminal.

---

# 🤖 Ollama Setup

The AI suggestion functionality uses Ollama locally.

Install Ollama and make the required model available.

Example:

```powershell
ollama pull phi
```

Then start the Ollama service:

```powershell
ollama serve
```

Run Streamlit in another terminal:

```powershell
streamlit run app.py
```

---

# 🧠 Why Version 1?

Version 1 was created to validate the core idea:

> Can a resume be processed automatically and evaluated for structure, skills, role relevance, formatting, and content improvements?

Once the core workflow was established, the project was redesigned into Version 2.

---

# 🔄 Next Version

➡️ **[Go to Version 2 — Next.js + FastAPI](../version-2-nextjs-fastapi)**

---

## 📌 Status

**Version:** 1.0 — Prototype

**Architecture:** Streamlit + Python

**AI:** Ollama
