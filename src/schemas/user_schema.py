"""This module handles user schemas."""
from datetime import datetime
from typing import ClassVar

from fastapi import status
from pydantic import BaseModel, EmailStr, Field, field_validator

from src.services.auth import is_valid_password
from src.utils.enumerators import UserType


class UserBaseSchema(BaseModel):
    """A schema class representing the base product."""
    email: EmailStr = Field(examples=["YourEmail@outlook.com"])
    password: str = Field(examples=["Your password."], min_length=8, max_length=25)
    user_type: UserType = Field(default=UserType.ANONYMOUS, examples=[UserType.ANONYMOUS.value])


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


class UserResponseSchema(UserBaseSchema):
    """A schema class for user response."""
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

    class Config:
        """SQLalchemy pydantic config class."""
        from_attributes = True
