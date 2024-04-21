import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    

settings = Settings()
