from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    client_id: str
    client_secret: str

    class Config:  # Capitalized 'C'
        env_file = '.env'

@lru_cache()
def get_settings():
    return Settings()


