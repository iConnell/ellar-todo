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


@Controller
class UsersController(ControllerBase):
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    @post("/", response={201: UserSerializer})
    def user_signup(self, user_details: UserSerializer):
        user = self.user_service.user_signup(user_details)
        return user

    @get("/", response={200: t.List[RetrieveUserSerilizer]})
    def list_users(self):
        return self.user_service.list_users()
