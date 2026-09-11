from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_resume_text(path: Path):
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join((p.extract_text() or "") for p in reader.pages)

    if path.suffix.lower() == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)

    return path.read_text(encoding="utf-8", errors="ignore")
