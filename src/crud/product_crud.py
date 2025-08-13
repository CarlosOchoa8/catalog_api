"""
Generate an Object of CRUD for products
"""

from src.crud.base_crud import CRUDBase
from src.models import Product


class CRUDProduct(CRUDBase):
    """Product CRUD class.
    :param CRUDBase: base CRUD."""


product_crud = CRUDProduct(Product)
