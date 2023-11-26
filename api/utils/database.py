from functools import lru_cache

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

from api import config
from api.activities.models import metadata as activities_metadata
from api.users.models import metadata as users_metadata


@lru_cache()
def setting():
    return config.Setting()


def database_psql_url_config():
    conf = Config(".env")
    return str(
        conf("DB_CONNECTION")
        + "://"
        + conf("DB_USERNAME")
        + ":"
        + conf("DB_PASSWORD")
        + "@"
        + conf("DB_HOST")
        + ":"
        + conf("DB_PORT")
        + "/"
        + conf("DB_DATABASE")
    )


database = databases.Database(database_psql_url_config())
engine = sqlalchemy.create_engine(database_psql_url_config())
users_metadata.create_all(engine)
activities_metadata.create_all(engine)

conn = engine.connect()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
