from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_host : str
    database_port : str
    database_password:str
    database_user:str
    database_name: str
    access_key: str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()