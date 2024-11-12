from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_SESSION_TOKEN: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    OPENSEARCH_ENDPOINT_URL: Optional[str] = None
    OPENSEARCH_ADMIN_USERNAME: Optional[str] = None
    OPENSEARCH_ADMIN_PASSWORD: Optional[str] = None


@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = GlobalConfig
    return configs()


config = get_config(BaseConfig().ENV_STATE)
