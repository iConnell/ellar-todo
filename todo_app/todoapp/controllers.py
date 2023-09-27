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
from ellar.common import Body


@Controller
class TodoappController(ControllerBase):
    def __init__(self, db: DummyTodoDB):
        self.todo_db = db

    @get("/")
    def index(self):
        return {"detail": "Welcome Todoapp Resource"}

    @post("/create", response={200: str})
    async def create_todo(self, payload: TodoSerializer):
        print("In the beninging")
        pk = await self.todo_db.add_todo(payload.dict())
        return pk
