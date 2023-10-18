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
from ellar.common import DataclassSerializer, Serializer


class UserSerializer(Serializer):
    first_name: str
    last_name: str
    username: str


class RetrieveUserSerilizer(UserSerializer):
    id: str
