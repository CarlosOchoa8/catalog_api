"""Application configuration settings module."""
import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    """
    Authentication settings.
    """
    SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    ALGORITHM = os.getenv('AUTH_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))


AUTHSETTINGS = AuthSettings()
