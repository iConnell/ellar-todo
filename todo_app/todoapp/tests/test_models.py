from todo_app.db.models import Todo
from todo_app.db.database import get_session_maker


class TestTodoModels:
    def test_todo_has_default_values(self, db, create_user):
        session = get_session_maker(db)()

        new_todo = Todo(title="Test Todo", description="A simple todo test", owner=create_user.id)
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)

        assert new_todo.id
        assert new_todo.created_at
        assert new_todo.completed == False
