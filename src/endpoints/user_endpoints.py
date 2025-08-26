"""This module handles User endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud
from src.helpers.db import get_db
from src.middlewares.exceptions import AlreadyExistException
from src.models import User
from src.schemas import UserCreateSchema, UserResponseSchema
from src.services.auth import get_current_user
from src.services.auth.services import require_admin_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[
        Depends(require_admin_user),
        Depends(get_current_user)
        ]
    )
currentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=UserResponseSchema)
async def create_user(
    user_in: UserCreateSchema,
    current_user: currentUser,
    db: AsyncSession = Depends(get_db)
    ) -> UserResponseSchema:
    """Add new user if doesn't exist.\n
    :param user_in: UserCreateSchema schema input.\n
    :return: UserResponseSchema response."""
    try:
        if await user_crud.get_by_email(email=user_in.email, db=db):
            raise AlreadyExistException(message="Invalid email.")

        user = await user_crud.create(db=db, obj_in=user_in.model_dump())
        return UserResponseSchema.model_validate(user)

    except Exception as exc:
        raise exc


user_router = router
