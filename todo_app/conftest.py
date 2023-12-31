import os
import asyncio
import pytest
from ellar.common.constants import ELLAR_CONFIG_MODULE
from ellar.core import App
from ellar.testing import Test
from ellar.testing.module import TestingModule
from httpx import AsyncClient
from .db.models import User

# from fullview_trader.db.cli.handlers import upgrade
from .db.models import Base
from .db.database import get_engine, get_session_maker
from .root_module import ApplicationModule

os.environ.setdefault(ELLAR_CONFIG_MODULE, "todo_app.config:TestConfig")


@pytest.fixture(scope="session")
def test_module() -> TestingModule:
    return Test.create_test_module(modules=[ApplicationModule])


@pytest.fixture(scope="session")
def app(test_module: TestingModule) -> App:
    return test_module.create_application()


@pytest.fixture(scope="session")
def client(app: App) -> AsyncClient:  # type: ignore[misc]
    with AsyncClient(app=app, base_url="http://testserver.com") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _db_engine(app: App):
    engine = get_engine(app.config)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db(app: App, _db_engine):
    """yields a SQLAlchemy connection which is rollback after the test"""
    yield app.config


@pytest.fixture()
def create_user(app: App):
    session = get_session_maker(app.config)()
    user_data = {"first_name": "First Name", "last_name": "Last Name", "username": "test_username"}

    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    yield user
    session.query(User).filter(User.id == user.id).delete()
    session.commit()
