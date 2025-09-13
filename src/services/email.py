"""This module handle service for email sending."""
import os
from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig, FastMail
from src.config.core import core_settings
from typing import List

class EmailSchema(BaseModel):
    """Schema model for Email sending."""
    email: List[EmailStr]


class EmailService:
    """This class handle emailing."""

    _conf = ConnectionConfig(
        MAIL_USERNAME = os.getenv("APP_MAIL"),
        MAIL_PASSWORD = os.getenv("APP_MAIL_PASSWORD"),
        MAIL_FROM = os.getenv("APP_MAIL"),
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_FROM_NAME = core_settings.APP_NAME,
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )


    @staticmethod
    def send_message() -> None:
        """Send email message from FastMail as background task."""
        print("Mandando mensaje...")
        print("Enviado")
