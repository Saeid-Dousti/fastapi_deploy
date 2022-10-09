# minute 9:10, Enviromental variable

from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str  
    database_name: str #database within postgres we are connecting to
    database_username: str
    secret_key: str   
    algorithm: str
    access_token_expire_minutes: int  

    class Config:
        env_file = ".env"

settings = Settings() 