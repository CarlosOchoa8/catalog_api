"""Application configuration settings module."""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    """
    Application configuration settings.
    """

    # APP_SETTINGS
    APP_NAME: str = Field(default="Product Catalog API", description="Basic catalog system to manage products.")
    VERSION: str = Field(default="0.1.0", description="Application version")


    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        description="CORS origins",
    )

core_settings = CoreSettings()
