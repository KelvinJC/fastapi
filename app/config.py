from pydantic import BaseSettings

class Settings(BaseSettings):
    '''
    A pydantic model to help validate incoming environment variables.
    Pydantic is case insensitive
    '''
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file=".env"



settings = Settings()

