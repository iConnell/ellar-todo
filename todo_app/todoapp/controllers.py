"""
Define endpoints routes in python class-based fashion
example:

@Controller("/dogs", tag="Dogs", description="Dogs Resources")
class MyController(ControllerBase):
    @get('/')
    def index(self):
        return {'detail': "Welcome Dog's Resources"}
"""
from ellar.common import Controller, ControllerBase, get, post, patch, delete, Provide
from ellar.common.exceptions import NotFound
from .schemas import TodoSerializer, RetrieveTodoSerializer
from .services import TodoService
import typing as t


from ..db.database import engine, SessionLocal
from ..db.models import Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


@Controller
class TodoappController(ControllerBase):
    def __init__(self, todo_service: TodoService) -> None:
        self.todo_service = todo_service

    @post("/create", response={201: RetrieveTodoSerializer})
    async def create_todo(self, todo_data: TodoSerializer):
        todo = self.todo_service.add_todo(todo_data)
        return todo

    @get("/", response={200: t.List[RetrieveTodoSerializer]})
    def list_todo(self):
        return self.todo_service.list_todos()

    @get("/{todo_id:str}", response={200: RetrieveTodoSerializer})
    async def get_todo(self, todo_id: int):
        todo = self.todo_service.get_todo(todo_id)
        if not todo:
            raise NotFound(f"Todo with id {todo_id} not found")

        return todo

    @patch("/{todo_id:str}", response={200: RetrieveTodoSerializer})
    async def update_todo(self, todo_id: str, payload: dict):
        todo = self.todo_service.update_todo(todo_id, payload)
        if not todo:
            raise NotFound(f"Todo with id {todo_id} not found")
        return todo

    @delete("/{todo_id:str}", response={204: dict})
    async def delete_todo(self, todo_id: str):
        todo = self.todo_service.delete_todo(todo_id)
        if not todo:
            raise NotFound(f"Todo with id {todo_id} not found")
        return 204, {}
