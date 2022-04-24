from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    environment: str
    database_url: str

    class Config:  # type: ignore
        env_file = ".env"
