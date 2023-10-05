"""
Define Serializers/DTOs
Example:

class ASampleDTO(Serializer):
    name: str
    age: t.Optional[int] = None

for dataclasses, Inherit from DataclassSerializer

@dataclass
class ASampleDTO(DataclassSerializer):
    name: str
    age: t.Optional[int] = None
"""
from ellar.common import Serializer


class TodoSerializer(Serializer):
    title: str
    description: str
    completed: bool = False


class RetrieveTodoSerializer(TodoSerializer):
    id: int
    # completed_at: str
    # created_at: str
