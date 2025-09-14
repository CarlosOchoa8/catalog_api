"""This module handle service for email sending."""
import os
from typing import List, Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from src.config.core import core_settings
from src.utils.logger import get_logger


logger = get_logger()


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


    @classmethod
    async def send_message(cls, message: Optional[str] = None) -> None:
        """Send email message from FastMail as background task."""
        try:
            print("Mandando mensaje...")
            print("Enviado")
            print(message)
            fm = FastMail(config=cls._conf)

            await fm.send_message(
                MessageSchema(
                    recipients=["ochoa.carlos8@outlook.com"],
                    subject="Test desde pytyhon fastapi",
                    body="""<p>Hi this test mail, thanks for using Fastapi-mail</p> """,
                    subtype=MessageType.html
                )
            )
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
