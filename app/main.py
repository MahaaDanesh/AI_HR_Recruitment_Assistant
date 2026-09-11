from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil, uuid

from .db import init_db, create_job, list_jobs, get_job
from .resume_parser import extract_resume_text
from .matcher import match_candidate
from .llm import generate_interview_questions, answer_hr_question
from .rag import add_document, search_knowledge

BASE = Path(__file__).resolve().parent.parent
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

app = FastAPI(title="AI HR Recruitment Assistant")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/api/jobs")
def jobs():
    return list_jobs()

@app.post("/api/jobs")
def new_job(title: str = Form(...), description: str = Form(...), skills: str = Form(...), experience: str = Form("")):
    return create_job(title, description, skills, experience)

@app.post("/api/screen")
async def screen(job_id: int = Form(...), resume: UploadFile = File(...)):
    job = get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    ext = Path(resume.filename or "").suffix.lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(400, "Only PDF and DOCX resumes are supported")

    saved = UPLOADS / f"{uuid.uuid4().hex}{ext}"
    with saved.open("wb") as f:
        shutil.copyfileobj(resume.file, f)

    text = extract_resume_text(saved)
    result = match_candidate(text, job)
    result["filename"] = resume.filename
    return result

@app.post("/api/interview")
async def interview(job_title: str = Form(...), job_description: str = Form(...), resume_text: str = Form(...), difficulty: str = Form("medium")):
    questions = generate_interview_questions(job_title, job_description, resume_text, difficulty)
    return {"questions": questions}

@app.post("/api/knowledge")
async def knowledge(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(400, "Use PDF, DOCX or TXT")
    saved = UPLOADS / f"{uuid.uuid4().hex}{ext}"
    with saved.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    text = extract_resume_text(saved)
    add_document(file.filename, text)
    return {"message": "Knowledge document added", "filename": file.filename}

@app.post("/api/ask")
def ask(question: str = Form(...)):
    contexts = search_knowledge(question)
    return {"answer": answer_hr_question(question, contexts), "sources": contexts}
