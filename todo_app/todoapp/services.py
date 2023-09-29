"""
Create a provider and declare its scope

@injectable
class AProvider
    pass

@injectable(scope=transient_scope)
class BProvider
    pass
"""
from ellar.di import injectable, singleton_scope
import typing as t
import uuid
from ..db.models import Todo


class DummyDBItem:
    pk: str

    def __init__(self, **data: t.Dict) -> None:
        self.__dict__ = data

    def __eq__(self, other) -> bool:
        if isinstance(other, DummyDBItem):
            return self.pk == other.pk
        return self.pk == str(other)


@injectable(scope=singleton_scope)
class DummyTodoDB:
    def __init__(self) -> None:
        self._data: t.List[DummyDBItem] = []

    def add_todo(self, data: t.Dict) -> str:
        pk = uuid.uuid4()
        _data = dict(data)
        _data.update(pk=str(pk))
        item = DummyDBItem(**_data)
        self._data.append(item)
        return item

    def list_todos(self) -> t.List[DummyDBItem]:
        return self._data

    def get_todo(self, todo_id):
        return self._data[self._data.index(todo_id)]

    def update_todo(self, todo_id, update_data):
        todo = self._data[self._data.index(todo_id)]
        todo.update(update_data)
        return todo

    def delete_todo(self, todo_id):
        return self._data.pop(self._data.index(todo_id))
