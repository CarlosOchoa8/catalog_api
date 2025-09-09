"""This module tries to audit actions."""
import inspect

from fastapi import Request

from src.middlewares.exceptions import AppException
from src.models import AuditLog
from src.utils.logger import get_logger

logger = get_logger()


class AuditService:
    """Audition logging service."""

    @staticmethod
    async def register(*args, **kwargs) -> None:
        """Register actions completed from endpoint and store them.\n
        :Arg user: user db obj.
        :Arg db: Async db connection.
        :Arg req: Request object.
        :Arg action: Main action func performed to been tracked.
        :Arg data[optional]: Any data to being store or changed in db.
        """
        try:
            user = kwargs.get("current_user")
            db = kwargs.get("db")
            req: Request = kwargs.get("request")
            action = kwargs.get("action")
            data = kwargs.get("data")
            print("++DATA QUE ESTOY MANDNDO =>", data)
            print("++REQUEST =>", req)

            obj_data = {
                "user_id": user.id or None,
                "action_performed":action.__qualname__,
                "affected_module":action.__self__.__class__.__name__,
                "ip_address":req.headers.get("X-Forwarded-For") or req.client.host,
                "user_agent":req.headers.get("user-agent"),
            }

            audit_obj = AuditLog(**obj_data)

            db.add(audit_obj)
            await db.commit()

        except Exception as e:
            logger.error(f"An unexpected error handling logs has occurred. {e}")
