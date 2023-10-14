from todo_app.todoapp.controllers import TodoController
from todo_app.todoapp.schemas import TodoSerializer
from todo_app.todoapp.services import TodoService
import pytest, json
from unittest import mock
from ellar.testing import Test, TestClient

# from unittest.mock import patch
from ellar.di import ProviderConfig

# from ellar.testing import Test


class TestTodoController:
    def setup_method(self):
        self.test_module = Test.create_test_module(controllers=[TodoController], providers=[TodoService])

        self.controller = self.test_module.get(TodoController)
        self.todo_data = {"title": "Test Todo", "description": "A simple create todo test"}

    def test_create_todo(self, db):
        todo_data = {"title": "Test Todo", "description": "A simple create todo test"}

        result = self.controller.create_todo(TodoSerializer(**todo_data))

        assert result.id == 1
        assert result.title == todo_data["title"]
        assert result.description == todo_data["description"]
        assert result.completed == False

    def test_list_todo(self, db):
        result = self.controller.list_todo()

        assert len(result) == 1

    def test_get_todo(self, db):
        result = self.controller.get_todo(1)

        assert result.id == 1
        assert result.title == self.todo_data["title"]
        assert result.description == self.todo_data["description"]
        assert result.completed == False

    def test_update_todo(self, db):
        update_data = {"title": "New Title", "description": "Different Description"}
        result = self.controller.update_todo(1, update_data)

        assert result.id == 1
        assert result.title == update_data["title"]
        assert result.description == update_data["description"]
        assert result.completed == False

    def test_delete_todo(self, db):
        status_code, result = self.controller.delete_todo(1)

        assert status_code == 204


class TestTodoControllerE2E:
    def setup_method(self):
        test_module = Test.create_test_module(
            controllers=[TodoController], providers=[ProviderConfig(TodoService, use_class=TodoService)]
        )
        self.client: TestClient = test_module.get_test_client()

        self.todo_data = todo_data = {"title": "Test Todo", "description": "A simple todo"}

    def test_create_todo(self):
        res = self.client.post("/todo/", data=json.dumps(self.todo_data))
        assert res.status_code == 201
        res_data = res.json()

        assert res_data["id"]
        assert res_data["title"] == self.todo_data["title"]
        assert res_data["description"] == self.todo_data["description"]
        assert res_data["completed"] == False

    def test_list_todo(self):
        res = self.client.get("/todo/")

        res_data = res.json()

        assert res.status_code == 200
        assert len(res_data) == 1

        assert res_data[0]["id"]
        assert res_data[0]["title"] == self.todo_data["title"]
        assert res_data[0]["description"] == self.todo_data["description"]
        assert res_data[0]["completed"] == False

    def test_get_todo(self):
        res = self.client.get("/todo/1")

        res_data = res.json()

        assert res.status_code == 200
        assert res_data["id"]
        assert res_data["title"] == self.todo_data["title"]
        assert res_data["description"] == self.todo_data["description"]
        assert res_data["completed"] == False

    def test_update_todo(self):
        update_data = {"title": "New Title", "description": "Different Description"}

        res = self.client.patch("/todo/1", data=json.dumps(update_data))
        res_data = res.json()

        assert res.status_code == 200
        assert res_data["id"]
        assert res_data["title"] == update_data["title"]
        assert res_data["description"] == update_data["description"]

    def test_delete_todo(self):
        res = self.client.delete("/todo/1")

        assert res.status_code == 204
