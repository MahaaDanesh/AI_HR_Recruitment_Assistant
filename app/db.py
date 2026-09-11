import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "recruitment.db"

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    c.execute("""CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        skills TEXT NOT NULL,
        experience TEXT
    )""")
    c.commit()
    c.close()

def create_job(title, description, skills, experience):
    c = conn()
    cur = c.execute("INSERT INTO jobs(title,description,skills,experience) VALUES(?,?,?,?)",
                    (title, description, skills, experience))
    c.commit()
    job = dict(c.execute("SELECT * FROM jobs WHERE id=?", (cur.lastrowid,)).fetchone())
    c.close()
    return job

def list_jobs():
    c = conn()
    rows = [dict(x) for x in c.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()]
    c.close()
    return rows

def get_job(job_id):
    c = conn()
    row = c.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    c.close()
    return dict(row) if row else None
