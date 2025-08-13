"""User endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import product_crud, user_crud
from src.helpers.db import get_db
from src.schemas import (ProductCreateSchema, ProductUpdateSchema,
                         UserCreateSchema, UserUpdateSchema)

router = APIRouter()


@router.post("/", response_model=UserCreateSchema)
async def create(user_in: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> UserCreateSchema:
    """Register new user."""
    try:
        return await user_crud.create(db=db, obj_in=user_in.model_dump())

    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Some problemas has ocurred.",
        ) from exc


user_router = router
