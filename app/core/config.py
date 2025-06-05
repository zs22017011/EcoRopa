from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = "postgresql+psycopg2://ecoropa:ecoropa@localhost:5432/ecoropa"
    SECRET_KEY: str = "super-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
