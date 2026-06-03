import os
from pathlib import Path

from models import Project, Tag
from sqlalchemy.orm import Session

SUPPORTED_INDICATORS = {
    "package.json": ["Node.js", "Frontend"],
    "requirements.txt": ["Python", "Backend"],
    "pyproject.toml": ["Python", "Modern-Python"],
    "Cargo.toml": ["Rust", "Systems"],
    "go.mod": ["Go"],
    ".git": ["Git-Managed"],
}


def scan_workspace(workspace_path: str, db: Session):
    path = Path(workspace_path)
    if not path.exists():
        return

    for item in path.iterdir():
        if item.is_dir():
            project_name = item.name
            project_path = str(item.resolve())

            detected_tags = []
            for file_indicator, tags in SUPPORTED_INDICATORS.items():
                if (item / file_indicator).exists():
                    detected_tags.extend(tags)

            detected_tags = list(set(detected_tags))

            db_project = db.query(Project).filter(Project.path == project_path).first()
            if not db_project:
                db_project = Project(name=project_name, path=project_path)
                db.add(db_project)
                db.commit()
                db.refresh(db_project)

            for tag_name in detected_tags:
                db_tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not db_tag:
                    db_tag = Tag(name=tag_name)
                    db.add(db_tag)
                    db.commit()
                    db.refresh(db_tag)

                if db_tag not in db_project.tags:
                    db_project.tags.append(db_tag)

            db.commit()
