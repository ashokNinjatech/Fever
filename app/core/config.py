from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fever Events Microservice"
    DESCRIPTION: str = "Microservice to fetch and cache event data from an external provider."
    VERSION: str = "1.0.0"
    PROVIDER_URL: str = "https://provider.code-challenge.feverup.com/api/events"
    REDIS_URL: str = "redis://localhost"

settings = Settings()
