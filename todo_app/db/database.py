# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import TestConfig
from ellar.core import Config


def get_engine(config: Config):
    engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
    return engine


def get_session_maker(config: Config):
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=get_engine(config))
    return session_local
