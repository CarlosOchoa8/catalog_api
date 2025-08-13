from pydantic import BaseModel, Field, PositiveFloat


class ProductBaseSchema(BaseModel):
    """A schema class representing the base product."""
    sku: str = Field(examples="PROD-0001")
    name: str = Field(examples="Your Product Name.")
    price: PositiveFloat
    brand: str = Field(examples="Your Recognized Brand.")

class ProductCreateSchema(ProductBaseSchema):
    """A schema class representing the base product."""

class ProductUpdateSchema(ProductBaseSchema):
    """A schema class representing response for product."""
