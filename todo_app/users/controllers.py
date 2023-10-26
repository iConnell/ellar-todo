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
import typing as t
from .schemas import UserSerializer, RetrieveUserSerilizer
from .services import UserService
from ..db.models import User


@Controller
class UsersController(ControllerBase):
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    @post("/", response={201: RetrieveUserSerilizer})
    def user_signup(self, user_details: UserSerializer) -> RetrieveUserSerilizer:
        user = self.user_service.user_signup(user_details)
        return user

    @get("/", response={200: t.List[RetrieveUserSerilizer]})
    def list_users(self) -> t.List[RetrieveUserSerilizer]:
        return self.user_service.list_users()

    @get("/{user_id:int}", response={200: RetrieveUserSerilizer})
    def get_user(self, user_id: int) -> RetrieveUserSerilizer:
        return self.user_service.get_user(user_id)
