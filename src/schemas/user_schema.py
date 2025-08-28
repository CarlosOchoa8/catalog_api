"""This module handles user schemas."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.services.auth import get_password_hash, is_valid_password
from src.utils.enumerators import UserType


class UserBaseSchema(BaseModel):
    """A schema class representing the base product."""
    email: EmailStr = Field(examples=["YourEmail@outlook.com"])
    password: str = Field(examples=["Your password."], min_length=8, max_length=25)
    user_type: UserType = Field(default=UserType.ANONYMOUS.value, examples=[UserType.ANONYMOUS.value])


class UserCreateSchema(UserBaseSchema):
    """A schema class for user creation."""

    @field_validator("password")
    @classmethod
    def validate_password(cls, value) -> str:
        """Check valid password rules"""
        if not is_valid_password(password=value):
            raise ValueError(
                "The password must have 8 to 25 characters, 1 uppercase letter, 1 lowercase, \n letter, 1 number, 1 special character (! @ # $ % & * . _), and must not contain spaces.",
            )
        return value


class UserUpdateSchema(UserCreateSchema):
    """A schema class for user updating."""
    email: Optional[EmailStr] = Field(default=None, examples=["YourEmail@outlook.com"])
    password: Optional[str] = Field(default=None, examples=["MyPassword456#"])
    user_type: Optional[UserType] = Field(default=None, examples=[UserType.ADMIN.value, UserType.ANONYMOUS.value])

    @field_validator("password")
    @classmethod
    def hash_password(cls, value) -> str:
        """Hash password if comes in schema data."""
        value = get_password_hash(plain_password=value)
        return value

    @field_validator("user_type")
    @classmethod
    def extract_value(cls, enum_class) -> str:
        """Extract the value of UserTypeEnum."""
        return enum_class.value


class UserResponseSchema(UserBaseSchema):
    """A schema class for user response."""
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    class Config:
        """SQLalchemy pydantic config class."""
        from_attributes = True


class ListUserResponseSchema(BaseModel):
    """A schema class for user list response."""
    user_data: List[UserResponseSchema]
    total: int
    page: int
