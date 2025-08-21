"""This module handles all endpoints routers."""
from fastapi import APIRouter

from src.endpoints import auth_router, product_router, user_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(user_router)
