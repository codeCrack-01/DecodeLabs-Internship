from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./dev_tracker.db"

engine = create_engine(
    str(SQLALCHEMY_DATABASE_URL), connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    import models

    models.Base.metadata.create_all(bind=engine)
