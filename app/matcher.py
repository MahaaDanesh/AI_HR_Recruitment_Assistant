import re
from .llm import ai_match

def normalize(s):
    return re.sub(r"[^a-z0-9+#.]", " ", s.lower())

def local_match(resume_text, job):
    resume = normalize(resume_text)
    required = [x.strip() for x in job["skills"].split(",") if x.strip()]
    matched, missing = [], []

    for skill in required:
        if normalize(skill).strip() in resume:
            matched.append(skill)
        else:
            missing.append(skill)

    score = round((len(matched) / max(len(required), 1)) * 100)
    return {
        "candidate_name": "Candidate",
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "experience_relevance": "Needs recruiter review",
        "recommendation": "Strong match" if score >= 75 else "Review candidate",
        "explanation": f"{len(matched)} of {len(required)} required skills were found.",
        "resume_text": resume_text
    }

def match_candidate(resume_text, job):
    result = ai_match(resume_text, job)
    if result:
        result["resume_text"] = resume_text
        return result
    return local_match(resume_text, job)
