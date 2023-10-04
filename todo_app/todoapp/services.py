"""
Create a provider and declare its scope

@injectable
class AProvider
    pass

@injectable(scope=transient_scope)
class BProvider
    pass
"""
from ellar.di import injectable, singleton_scope, request_scope
import typing as t
from ..db.models import Todo
from ..db.database import SessionLocal


@injectable(scope=singleton_scope)
class TodoService:
    def __init__(self) -> None:
        self.db = SessionLocal()

    def add_todo(self, todo_data):
        new_todo = Todo(title=todo_data.title, description=todo_data.description)
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo

    def list_todos(self):
        todos = self.db.query(Todo).all()
        print(todos)
        return todos

    def get_todo(self, todo_id):
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def update_todo(self, todo_id, update_data):
        todo = self.db.query(Todo).filter(Todo.id == todo_id)

        todo.update(update_data)
        self.db.commit()

        return todo.first()

    def delete_todo(self, todo_id):
        delete_count = self.db.query(Todo).filter(Todo.id == todo_id).delete()
        self.db.commit()

        return delete_count
