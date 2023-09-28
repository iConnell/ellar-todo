from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, Column, UUID
from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
