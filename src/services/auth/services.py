"""This module handles auth funcs."""
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import exceptions, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from src import models
from src.helpers.db import get_db
from src.utils.enumerators import UserType

from .settings import AUTHSETTINGS

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
AUTH_SECRET_KEY = AUTHSETTINGS.SECRET_KEY
AUTH_ALGORITHM = AUTHSETTINGS.ALGORITHM
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = AUTHSETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES


def is_valid_password(password: str) -> Any:
    """Validate password against regex pattern rules.\n
    :param password: Plain text password to validate.\n
    :return: Match object if valid."""
    regex = re.compile(
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*._])(?!.*\s).{8,25}$"
    )
    return re.fullmatch(regex, password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password.
    :param plain_password: Plain text password to verify.
    :param hashed_password: Hashed password from database.
    :return: True if passwords match, False otherwise."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    """Generate hash from plain text password.\n
    :param plain_password: Plain text password to hash.\n
    :return: Hashed password string."""
    return pwd_context.hash(plain_password)


async def authenticate_user(email: str, password: str, db: AsyncSession) -> models.User | bool:
    """Authenticate user by email and password validation.\n
    :param email: User email address.\n
    :param password: Plain text password.\n
    :param db: Async database session.\n
    :return: User object if credentials are valid, False otherwise."""
    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalar_one_or_none()
    stmt = select(models.User).where(models.User.email == email)
    user = await db.scalar(stmt)

    if user:
        return user if verify_password(password, user.password) else False
    return False


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
) -> models.User:
    """Extract and validate current user from JWT token.\n
    :param db: Async database session dependency.\n
    :param credentials: HTTP Bearer token credentials.\n
    :return: Authenticated user object."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        user_email = payload.get("email")

        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        stmt = select(models.User).options(
            defer(models.User.password)
            ).where(models.User.email == user_email)
        user = await db.scalar(stmt)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except exceptions.JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Problem with credentials occurred. {str(exc)}",
        ) from exc


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token with expiration time.
    :param data: Payload data to encode in token.
    :param expires_delta: Custom expiration time delta.
    :return: Encoded JWT token string."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode["exp"] = expire
    return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)


async def generate_token(db: AsyncSession, email: str, password: str) -> str:
    """Generate JWT access token for authenticated user.
    :param db: Async database session.
    :param email: User email address.
    :param password: Plain text password.
    :return: JWT access token string."""
    db_user = await authenticate_user(email=email, password=password, db=db)

    if db_user:
        access_token_expires = timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "id": str(db_user.id),  # type: ignore
            "email": str(db_user.email)  # type: ignore
        }

        return create_access_token(data=payload, expires_delta=access_token_expires)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='El usuario o la contraseña no coinciden',
    )


async def validate_token(token: str) -> None:
    """Validate JWT token signature and expiration.
    :param token: JWT token string to validate.
    :return: None if valid, JSONResponse with error if invalid."""
    try:
        jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
    except exceptions.ExpiredSignatureError:
        return JSONResponse(
            content={"message": "Token Expired"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except exceptions.JWTError as jwt_error:
        return JSONResponse(
            content={"message": "Unable to validate token",
                     "detail": str(jwt_error)},
            status_code=status.HTTP_401_UNAUTHORIZED
        )


async def require_admin_user(current_user: models.User) -> None:
    """Require authenticated user to have admin privileges.
    :param current_user: Current authenticated user dependency.
    :return: User object if admin, raises exception otherwise."""
    if current_user.user_type != UserType.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're not able to perform this.",
        )
