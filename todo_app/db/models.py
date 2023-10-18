from datetime import datetime
from sqlalchemy import Boolean, String, DateTime, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer, ForeignKey("users.id", name="fk_todo_owner"), nullable=False)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())

    todo_owner = relationship("User", back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String(15), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    todos = relationship("Todo", back_populates="todo_owner")
