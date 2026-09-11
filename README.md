# AI HR Recruitment Assistant

A student-friendly Agentic AI recruitment assistant built with FastAPI, SQLite, Gemini, ChromaDB and a simple HTML/CSS/JS dashboard.

## Features
- Create and manage job descriptions
- Upload multiple PDF/DOCX resumes
- Extract candidate information
- AI-assisted resume/job matching
- Explain matched and missing skills
- Candidate ranking
- Personalized interview question generation
- HR knowledge-base RAG
- Recruitment agent workflow

## Important
This is an AI-assisted screening tool. It should support recruiters, not make final employment decisions. Do not use protected/sensitive attributes for ranking.

## Setup

1. Create a virtual environment:
   Windows:
   `python -m venv venv`
   `venv\Scripts\activate`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Copy `.env.example` to `.env` and add your Gemini API key.

4. Start:
   `uvicorn app.main:app --reload`

5. Open:
   `http://127.0.0.1:8000`

If no Gemini key is configured, the app uses a deterministic local fallback for basic matching.
