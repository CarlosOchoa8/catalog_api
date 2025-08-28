"""This module handles User endpoints."""
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud
from src.helpers.db import get_db
from src.middlewares.exceptions import AlreadyExistException, NotFoundException
from src.models import User
from src.schemas import (ListUserResponseSchema, UserCreateSchema,
                         UserResponseSchema, UserUpdateSchema)
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

        user = await user_crud.create(db=db, obj_in=user_in.model_dump(exclude_unset=True))
        return UserResponseSchema.model_validate(user)

    except Exception as exc:
        raise exc


@router.get("/", response_model=ListUserResponseSchema)
async def get_users(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
    db: AsyncSession = Depends(get_db)
    ) -> ListUserResponseSchema:
    """Retrieve all users.\n
    :param offset: Records to find starting from.\n
    :param limit: Qty of records to being retrieved.\n
    :return: UserResponseSchema response."""
    try:
        users = await user_crud.get_multi(db=db, skip=offset, limit=limit)
        if not users:
            raise NotFoundException(
                message="Users not found."
            )

        return ListUserResponseSchema(
            user_data=users,
            total=len(users),
            page=(offset // limit) + 1 if limit else 1
        )

    except Exception as exc:
        raise exc


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
    ) -> UserResponseSchema:
    """Retrieve an user.\n
    :param user_id: user identifier.\n
    :return: UserResponseSchema response."""
    try:
        user = await user_crud.get(id=user_id, db=db)
        if not user:
            raise NotFoundException(
                message="User not found."
            )

        return user

    except Exception as exc:
        raise exc


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: UUID,
    user_in: UserUpdateSchema,
    db: AsyncSession = Depends(get_db)
    ) -> UserResponseSchema:
    """Retrieve an user.\n
    :param user_id: user identifier.\n
    :param user_in: user data to update.\n
    :return: UserResponseSchema response."""
    try:
        db_user = await user_crud.get(id=user_id, db=db)
        if not db_user:
            raise NotFoundException(
                message="User not found."
            )

        updated_user = await user_crud.update(db=db, db_obj=db_user, obj_in=user_in.model_dump(exclude_unset=True))
        return UserResponseSchema.model_validate(updated_user)

    except Exception as exc:
        raise exc


user_router = router
