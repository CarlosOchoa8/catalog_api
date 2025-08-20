"""This module handles Product endpoints operations."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import product_crud
from src.helpers.db import get_db
from src.models import User
from src.schemas import (ProductCreateSchema, ProductResponseSchema,
                         ProductUpdateSchema)
from src.services.auth import get_current_user
from src.services.auth.services import require_admin_user


router = APIRouter()


@router.post("/", response_model=ProductResponseSchema)
async def create_product(
    product_in: ProductCreateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Add new product if doesn't exist.\n
    :param product_in: ProductCreateSchema schema input.\n
    :return: Product created response."""
    try:
        await require_admin_user(current_user=current_user)

        if await product_crud.get_by_sku(sku=product_in.sku, db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SKU already exists.",
            )

        product = await product_crud.create(db=db, obj_in=product_in.model_dump())
        return ProductResponseSchema.model_validate(product)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error has occurred.",
        ) from exc


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Retrieve product by it's ID.\n
    :param product_id: productID.\n
    :return: ProductResponseSchema response."""
    try:
        product = await product_crud.get(db=db, id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return ProductResponseSchema.model_validate(product)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error has occurred.",
        ) from exc


@router.put("/{product_id}", response_model=ProductResponseSchema)
async def update_product(
    product_id: str,
    product_in: ProductUpdateSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Update product's info by it's ID.\n
    :param product_id: productID.\n
    :param product_in: ProductUpdateSchema input.\n
    :return: ProductResponseSchema response."""
    try:
        require_admin_user(current_user=current_user)

        db_product = await product_crud.get(db=db, id=product_id)
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        updated_product = await product_crud.update(
            db=db,
            db_obj=db_product,
            obj_in=product_in.model_dump(exclude_unset=True)
        )
        return ProductResponseSchema.model_validate(updated_product)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error has occurred.",
        ) from exc


product_router = router
