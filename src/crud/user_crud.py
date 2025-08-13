"""
Generate an Object of CRUD for users
"""

from src.crud.base_crud import CRUDBase
from src.models import User


class CRUDUser(CRUDBase):
    """User CRUD class.
    :param CRUDBase: base CRUD."""


user_crud = CRUDUser(User)
