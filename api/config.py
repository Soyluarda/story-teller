from pydantic import BaseSettings


class Setting(BaseSettings):
    DB_CONNECTION: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_DATABASE: str = "postgres"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"

