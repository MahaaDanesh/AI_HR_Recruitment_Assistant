import chromadb
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "chroma_db"
client = chromadb.PersistentClient(path=str(DB))
collection = client.get_or_create_collection("hr_knowledge")

def chunks(text, size=1200):
    return [text[i:i+size] for i in range(0, len(text), size)] or [""]

def add_document(filename, text):
    parts = chunks(text)
    ids = [f"{filename}-{i}" for i in range(len(parts))]
    collection.add(ids=ids, documents=parts, metadatas=[{"source": filename} for _ in parts])

def search_knowledge(question, n=4):
    if collection.count() == 0:
        return []
    result = collection.query(query_texts=[question], n_results=min(n, collection.count()))
    return result.get("documents", [[]])[0]
