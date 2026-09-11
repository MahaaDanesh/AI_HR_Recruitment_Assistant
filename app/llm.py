import os, json, re
from dotenv import load_dotenv

load_dotenv()

def client():
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your_api_key_here":
        return None
    from google import genai
    return genai.Client(api_key=key)

def ai_match(resume, job):
    c = client()
    if not c:
        return None

    prompt = f"""
You are an AI recruitment screening assistant. Evaluate a candidate against a job description.
Do not use or infer protected characteristics. Do not make a final hiring decision.
Return ONLY valid JSON with:
candidate_name, score (0-100), matched_skills, missing_skills,
experience_relevance, recommendation, explanation.

JOB TITLE: {job['title']}
JOB DESCRIPTION: {job['description']}
REQUIRED SKILLS: {job['skills']}
EXPERIENCE: {job['experience']}

RESUME:
{resume[:18000]}
"""
    try:
        r = c.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), contents=prompt)
        text = re.sub(r"^```json|^```|```$", "", r.text.strip(), flags=re.M).strip()
        return json.loads(text)
    except Exception:
        return None

def generate_interview_questions(title, description, resume, difficulty):
    c = client()
    if not c:
        return [
            "Explain one project from your resume that is most relevant to this role.",
            "What technical challenge did you face in that project and how did you solve it?",
            "Which required skill are you most confident in, and why?",
            "Describe a situation where you had to learn a new technology quickly.",
            "What would you improve in one of your previous projects?"
        ]

    prompt = f"""
Generate 8 interview questions for a {title} candidate.
Difficulty: {difficulty}
Use both the job description and candidate resume.
Include a mix of technical, project-based and behavioral questions.
Return ONLY a JSON array of strings.

JOB:
{description[:10000]}

RESUME:
{resume[:12000]}
"""
    try:
        r = c.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), contents=prompt)
        text = re.sub(r"^```json|^```|```$", "", r.text.strip(), flags=re.M).strip()
        return json.loads(text)
    except Exception:
        return ["Tell us about your most relevant project.", "Explain your strongest technical skill."]

def answer_hr_question(question, contexts):
    c = client()
    context = "\n\n".join(contexts)
    if not c:
        return "RAG context retrieved:\n" + (context[:3000] if context else "No HR knowledge documents found.")

    prompt = f"""
Answer the HR recruiter's question using ONLY the supplied knowledge context.
If the context does not contain the answer, say that the information is not available.
Question: {question}
Context:
{context[:12000]}
"""
    try:
        r = c.models.generate_content(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), contents=prompt)
        return r.text
    except Exception:
        return "Unable to generate an answer right now."
