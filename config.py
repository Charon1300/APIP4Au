from pydantic import AfterValidator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated

secretStr = Annotated[str, AfterValidator(PostgresDsn), AfterValidator(str)]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env", env_file_encoding = "utf-8")

    database_url: secretStr


settings = Settings() # loaded from .env