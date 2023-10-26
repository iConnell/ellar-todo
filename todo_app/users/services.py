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
from ..db.database import get_session_maker
from ..db.models import User
from ellar.core import Config
from ellar.common import HTTPException
import typing as t
from .schemas import UserSerializer


@injectable(scope=singleton_scope)
class UserService:
    def __init__(self, config: Config) -> None:
        session_maker = get_session_maker(config)
        self.db = session_maker()

    def user_signup(self, user_details: UserSerializer) -> User:
        if self.db.query(User).filter(User.username == user_details.username).first():
            raise HTTPException(status_code=400, detail=f"User with username {user_details.username} already exist")

        user = User(**dict(user_details))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self) -> t.List[User]:
        return self.db.query(User).all()

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
