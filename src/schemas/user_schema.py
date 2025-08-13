from pydantic import BaseModel
from pydantic import EmailStr, Field
from src.utils.enumerators import UserType


class UserBaseSchema(BaseModel):
    """A schema class representing the base product."""
    email: EmailStr = Field(examples=["someMail@outlook.com"])
    user_type: UserType = Field(default=UserType.ANONYMOUS, examples=[UserType.ANONYMOUS.value])

class UserCreateSchema(UserBaseSchema):
    """A schema class for user creation."""

class UserUpdateSchema(UserCreateSchema):
    """A schema class for user updating."""
