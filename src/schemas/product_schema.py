from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, PositiveFloat


class ProductBaseSchema(BaseModel):
    """A schema class representing the base product."""
    sku: str = Field(examples=["PROD-0001""PROD-0001"])
    name: str = Field(examples=["Your Product Name."])
    price: PositiveFloat
    brand: str = Field(examples=["Your Recognized Brand."])

class ProductCreateSchema(ProductBaseSchema):
    """A schema class representing the base product."""


class ProductUpdateSchema(ProductBaseSchema):
    """A schema class representing response for product."""


class ProductResponseSchema(ProductBaseSchema):
    """A schema class for product response."""
    created_at: datetime
    updated_at: datetime

    class Config:
        """SQLalchemy pydantic config class."""
        from_attributes = True

class ProductsResponseSchema(BaseModel):
    """A schema class products response."""
    products: List[ProductResponseSchema]
