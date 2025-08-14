from pydantic import BaseModel, EmailStr, Field


class UserAuthSchema(BaseModel):
    """A schema class for user authentication."""
    email: EmailStr = Field(examples=["YourEmail@outlook.com"])
    password: str


class TokenResponse(BaseModel):
    """A schema class for user creation."""
    access_token: str
    token_type: str
