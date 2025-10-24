from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.task import Base

DATABASE_URL = "postgresql+psycopg2://postgres:abdullah420@localhost/task"

engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(
    bind = engine,
    class_ = Session,
    expire_on_commit = False
)

def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
def init_db():
    Base.metadata.create_all(bind = engine)