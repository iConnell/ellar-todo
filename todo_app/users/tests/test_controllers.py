from todo_app.users.controllers import UsersController
from todo_app.users.schemas import UserSerializer
from todo_app.users.services import UserService
import json
from ellar.testing import Test, TestClient

# from unittest.mock import patch
from ellar.di import ProviderConfig


class TestUsersControllerE2E:
    def setup_method(self):
        test_module = Test.create_test_module(
            controllers=[UsersController], providers=[ProviderConfig(UserService, use_class=UserService)]
        )
        self.client: TestClient = test_module.get_test_client()

        self.user_data = {"first_name": "Test", "last_name": "User", "username": "test_user"}

    def test_create_user(self, db):
        res = self.client.post("/users/", data=json.dumps(self.user_data))
        assert res.status_code == 201

        res_data = res.json()

        assert res_data["id"]
        assert res_data["created_at"]
        assert res_data["first_name"] == self.user_data["first_name"]
        assert res_data["last_name"] == self.user_data["last_name"]
        assert res_data["username"] == self.user_data["username"]

    def test_list_user(self):
        res = self.client.get("/users/")

        res_data = res.json()

        assert res.status_code == 200
        assert len(res_data) == 1

        assert res_data[0]["id"]
        assert res_data[0]["created_at"]
        assert res_data[0]["first_name"] == self.user_data["first_name"]
        assert res_data[0]["last_name"] == self.user_data["last_name"]
        assert res_data[0]["username"] == self.user_data["username"]

    def test_get_user(self):
        res = self.client.get("/users/1")

        res_data = res.json()

        assert res.status_code == 200
        assert res_data["id"]
        assert res_data["created_at"]
        assert res_data["first_name"] == self.user_data["first_name"]
        assert res_data["last_name"] == self.user_data["last_name"]
        assert res_data["username"] == self.user_data["username"]
