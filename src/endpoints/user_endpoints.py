"""This module handles User endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud
from src.helpers.db import get_db
from src.models import User
from src.schemas import UserCreateSchema, UserResponseSchema
from src.services.auth import get_current_user
from src.services.auth.services import require_admin_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)
# currentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=UserResponseSchema)
async def create_user(
    user_in: UserCreateSchema,
    # current_user: currentUser,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ) -> UserResponseSchema:
    """Add new user if doesn't exist.\n
    :param user_in: UserCreateSchema schema input.\n
    :return: UserResponseSchema response."""
    try:
        print("YA ESTOY OBTENIENDO EL USUARIO", current_user)
        await require_admin_user(current_user=current_user)

        if await user_crud.get_by_email(email=user_in.email, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email.",
            )

        user = await user_crud.create(db=db, obj_in=user_in.model_dump())
        return UserResponseSchema.model_validate(user)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error has occurred.",
        ) from exc


user_router = router
