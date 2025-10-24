from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, Integer, String, Enum as SQLEnum, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TaskStatus(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    priority = Column(SQLEnum(TaskPriority), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    