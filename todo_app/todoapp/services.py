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
from ..db.database import get_session_maker
from ellar.core import Config


@injectable(scope=singleton_scope)
class TodoService:
    def __init__(self, config: Config) -> None:
        session_maker = get_session_maker(config)
        self.db = session_maker()

    def add_todo(self, todo_data):
        new_todo = Todo(**dict(todo_data))
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo

    def list_todos(self, user, completed):
        if not user:
            return self.db.query(Todo).filter(Todo.completed == completed).all()
        print(completed)
        return self.db.query(Todo).filter(Todo.owner == user, Todo.completed == completed).all()

    def get_todo(self, todo_id):
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def update_todo(self, todo_id, update_data, user):
        todo = self.db.query(Todo).filter(Todo.id == todo_id, Todo.owner == user)

        todo.update(update_data)
        self.db.commit()

        return todo.first()

    def delete_todo(self, todo_id, user):
        delete_count = self.db.query(Todo).filter(Todo.id == todo_id, Todo.owner == user).delete()
        self.db.commit()

        return delete_count
