from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

project_tag_association = Table(
    "project_tag",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    path = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_scanned = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tags = relationship(
        "Tag", secondary=project_tag_association, back_populates="projects"
    )
    sessions = relationship(
        "WorkSession", back_populates="project", cascade="all, delete-orphan"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    projects = relationship(
        "Project", secondary=project_tag_association, back_populates="tags"
    )


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    lines_changed = Column(Integer, default=0)

    project = relationship("Project", back_populates="sessions")
