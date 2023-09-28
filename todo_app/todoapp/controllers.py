"""
Define endpoints routes in python class-based fashion
example:

@Controller("/dogs", tag="Dogs", description="Dogs Resources")
class MyController(ControllerBase):
    @get('/')
    def index(self):
        return {'detail': "Welcome Dog's Resources"}
"""
from ellar.common import Controller, ControllerBase, get, post, patch, delete
from ellar.common.exceptions import NotFound
from .schemas import TodoSerializer, RetrieveTodoSerializer
from .services import DummyTodoDB
import typing as t


@Controller
class TodoappController(ControllerBase):
    def __init__(self, db: DummyTodoDB):
        self.todo_db = db

    @get("/", response={200: t.List[RetrieveTodoSerializer]})
    def list_todo(self):
        todos = self.todo_db._data
        return todos

    @post("/create", response={201: RetrieveTodoSerializer})
    async def create_todo(self, payload: TodoSerializer):
        todo = self.todo_db.add_todo(payload.dict())
        return todo

    @get("/{todo_id:str}", response={200: RetrieveTodoSerializer})
    async def get_todo(self, todo_id: str):
        todo = self.todo_db.get_todo(todo_id)
        return todo

    @patch("/{todo_id:str}", response={200: RetrieveTodoSerializer})
    async def update_todo(self, todo_id: str, payload: dict):
        todo = self.todo_db.update_todo(todo_id, payload)
        return todo

    @delete("/{todo_id:str}", response={204: dict})
    async def delete_todo(self, todo_id: str):
        todo = self.todo_db.delete_todo(todo_id)
        return 204, {}
