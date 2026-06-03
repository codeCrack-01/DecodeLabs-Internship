from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from bg_scan import scan_workspace
from db import SessionLocal, engine, init_db
from fastapi import BackgroundTasks, Depends, FastAPI
from models import Project, WorkSession
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Database initialized successfully!")

    yield
    print("Shutting down dev tracker backend...")


app = FastAPI(title="Local Dev-Tool Tracker", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/scan")
async def trigger_scan(
    workspace_path: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    background_tasks.add_task(scan_workspace, workspace_path, db)
    return {"status": "Scan initiated in the background for " + workspace_path}


@app.get("/projects")
async def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "path": p.path,
            "tags": [t.name for t in p.tags],
            "last_scanned": p.last_scanned,
        }
        for p in projects
    ]


@app.post("/projects/{project_id}/session")
async def log_session(
    project_id: int, minutes: int, lines: int = 0, db: Session = Depends(get_db)
):
    end = datetime.now()
    start = end - timedelta(minutes=minutes)

    session = WorkSession(
        project_id=project_id, start_time=start, end_time=end, lines_changed=lines
    )
    db.add(session)
    db.commit()
    return {"status": "Logged work session successfully"}
