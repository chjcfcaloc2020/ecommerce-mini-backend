from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  POSTGRES_USER: str
  POSTGRES_PASSWORD: str
  POSTGRES_HOST: str
  POSTGRES_PORT: int
  POSTGRES_DB: str

  PROJECT_NAME: str
  VERSION: str
  SECRET_KEY: str
  ALGORITHM: str
  ACCESS_TOKEN_EXPIRE_MINUTES: int

  model_config = SettingsConfigDict(env_file=".env", extra="ignore")

  @property
  def DATABASE_URL(self):
    return (
      f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
      f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    )

settings = Settings()