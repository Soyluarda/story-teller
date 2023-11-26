import databases
import sqlalchemy
from functools import lru_cache
from api import config
from api.models import metadata
from starlette.config import Config


@lru_cache()
def setting():
    return config.Setting()


def database_psql_url_config():
    conf = Config(".env")
    return str(conf("DB_CONNECTION") + "://" + conf("DB_USERNAME") + ":" + conf("DB_PASSWORD")
               + "@" + conf("DB_HOST") + ":" + conf("DB_PORT") + "/" + conf("DB_DATABASE"))

database = databases.Database(database_psql_url_config())
engine = sqlalchemy.create_engine(database_psql_url_config())
metadata.create_all(engine)
