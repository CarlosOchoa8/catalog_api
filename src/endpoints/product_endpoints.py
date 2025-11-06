"""This module handles Product endpoints operations."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import product_crud
from src.helpers.db import get_db
from src.middlewares.exceptions import (AlreadyExistException, AppException,
                                        NotFoundException)
from src.models import User
from src.schemas import (ProductCreateSchema, ProductResponseSchema,
                         ProductsResponseSchema, ProductUpdateSchema)
from src.services.audit import AuditService
from src.services.auth.services import get_current_user, require_admin_user
from src.services.email import EmailService


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)
currentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", dependencies=[Depends(require_admin_user)], response_model=ProductResponseSchema)
async def create_product(
    product_in: ProductCreateSchema,
    current_user: currentUser,
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> ProductResponseSchema:
    """Add new product if doesn't exist.\n
    :param product_in: ProductCreateSchema schema input.\n
    :return: ProductResponseSchema response."""
    try:
        if await product_crud.get_by_sku(sku=product_in.sku, db=db):
            raise AlreadyExistException(message="SKU already exists.")

        product = await product_crud.create(db=db, obj_in=product_in.model_dump())
        await AuditService.register(
            current_user=current_user, db=db, request=request,
            action=product_crud.create, data=product_in.model_dump()
            )

        return ProductResponseSchema.model_validate(product)

    except AppException as exc:
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

    except AppException as exc:
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

    except AppException as exc:
        raise exc


@router.put("/{product_id}", dependencies=[Depends(require_admin_user)], response_model=ProductResponseSchema)
async def update_product(
    product_id: UUID,
    product_in: ProductUpdateSchema,
    current_user: currentUser,
    request: Request,
    background_tasks: BackgroundTasks,
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

        if await product_crud.get_by_sku(sku=product_in.sku, db=db):
            raise AlreadyExistException(message="Sky already exists.")

        if await product_crud.get_by_name(name=product_in.name, db=db):
            raise AlreadyExistException(message="Name already exists.")

        updated_product = await product_crud.update(
            db=db,
            db_obj=db_product,
            obj_in=product_in.model_dump(exclude_unset=True)
        )
        await AuditService.register(
            current_user=current_user, db=db, request=request,
            action=product_crud.update, data=product_in.model_dump()
            )

        background_tasks.add_task(
            EmailService.notify_admin,
            message=f"Product {product_id} has been updated by user {current_user.id}"
            )

        return ProductResponseSchema.model_validate(updated_product)

    except AppException as exc:
        raise exc


product_router = router
