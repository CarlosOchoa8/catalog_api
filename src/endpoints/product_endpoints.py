"""This module handles Product endpoints operations."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import product_crud
from src.helpers.db import get_db
from src.middlewares.exceptions import (AlreadyExistException, ApiException,
                                        NotFoundException)
from src.models import User
from src.schemas import (ProductCreateSchema, ProductResponseSchema,
                         ProductsResponseSchema, ProductUpdateSchema)
from src.services.auth import get_current_user
from src.services.auth.services import require_admin_user


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
# currentUser = Annotated(User, Depends(get_current_user))


@router.post("/", dependencies=[Depends(require_admin_user)], response_model=ProductResponseSchema)
async def create_product(
    product_in: ProductCreateSchema,
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Add new product if doesn't exist.\n
    :param product_in: ProductCreateSchema schema input.\n
    :return: ProductResponseSchema response."""
    try:
        if await product_crud.get_by_sku(sku=product_in.sku, db=db):
            raise AlreadyExistException(message="SKU already exists.")

        product = await product_crud.create(db=db, obj_in=product_in.model_dump())
        return ProductResponseSchema.model_validate(product)

    except Exception as exc:
        raise exc


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Retrieve product by it's ID.\n
    :param product_id: productID.\n
    :return: ProductResponseSchema response."""
    try:
        product = await product_crud.get(db=db, id=product_id)
        if not product:
            raise NotFoundException(message="Product not found.")

        return ProductResponseSchema.model_validate(product)

    except Exception as exc:
        raise exc


@router.get("/", response_model=ProductsResponseSchema)
async def get_products(
    db: AsyncSession = Depends(get_db)
) -> ProductsResponseSchema:
    """Retrieve products.\n
    :return: ProductsResponseSchema response."""
    try:
        products = await product_crud.get_multi(db=db)
        if not products:
            raise NotFoundException(message="No products found.")

        return ProductsResponseSchema(
            products=[ProductResponseSchema.model_validate(prod) for prod in products]
            )

    except Exception as exc:
        raise exc


@router.put("/{product_id}", dependencies=[Depends(require_admin_user)], response_model=ProductResponseSchema)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Update product's info by it's ID.\n
    :param product_id: productID.\n
    :param product_in: ProductUpdateSchema input.\n
    :return: ProductResponseSchema response."""
    try:
        db_product = await product_crud.get(db=db, id=product_id)
        if not db_product:
            raise NotFoundException(message="Product not found.")

        updated_product = await product_crud.update(
            db=db,
            db_obj=db_product,
            obj_in=product_in.model_dump(exclude_unset=True)
        )
        return ProductResponseSchema.model_validate(updated_product)

    except Exception as exc:
        raise exc


product_router = router
