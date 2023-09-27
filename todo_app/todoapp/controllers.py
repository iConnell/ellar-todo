"""
Define endpoints routes in python class-based fashion
example:

@Controller("/dogs", tag="Dogs", description="Dogs Resources")
class MyController(ControllerBase):
    @get('/')
    def index(self):
        return {'detail': "Welcome Dog's Resources"}
"""
from ellar.common import Controller, ControllerBase, get, post
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

    @post("/create", response={200: RetrieveTodoSerializer})
    async def create_todo(self, payload: TodoSerializer):
        todo = self.todo_db.add_todo(payload.dict())
        return todo
