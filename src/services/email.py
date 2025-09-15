"""This module handle service for email sending."""
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Template
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from src.config.core import core_settings
from src.helpers.db import get_db
from src.models import User
from src.utils.enumerators import UserType
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
        VALIDATE_CERTS = True,
        TEMPLATE_FOLDER = Path(__file__).parent.parent / "utils" / "templates"
    )

    @classmethod
    async def notify_admin(cls, message: Optional[str] = None) -> None:
        """Send email notifications to ADMIN users.\n
        :param message: Message to be sent to users.
        :return: None."""
        try:
            async for db in get_db():
                fm = FastMail(config=cls._conf)

                stmt = select(User.email).filter(User.user_type == UserType.ADMIN.value)
                scalars = await db.scalars(stmt)
                user_receivers = scalars.all()

                rendered_html = cls._get_rendered_template(template_name="mail_notif.html", message=message)

                await fm.send_message(
                    MessageSchema(
                        recipients=user_receivers,
                        subject="System Notification",
                        # body=f"""<p>Hi this test mail, thanks for using Fastapi-mail : {message}</p> """,
                        body=rendered_html,
                        subtype=MessageType.html
                    )
                )

        except Exception as e:
            logger.error(f"Error enviando email: {e}")

    @classmethod
    def _get_rendered_template(cls, template_name: str, message: str) -> str:
        """Return html template by Jinja2.
        :param template_name: .html template file.
        :param message: Notification message to be sent.
        :return: str."""
        tmp_path = cls._conf.TEMPLATE_FOLDER/f"{template_name}"
        with open(tmp_path, 'r', encoding='utf-8') as tmp_file:
            template_content = tmp_file.read()

        template = Template(template_content)
        rendered_html = template.render(
            message=message or "System modifies.",
            date=datetime.now().strftime("%d/%m/%Y"),
            time=datetime.now().strftime("%H:%M:%S"),
            reference_id=f"REF-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            app_name=core_settings.APP_NAME,
        )

        return rendered_html
