"""This module handles all endpoints routers."""
from fastapi import APIRouter
from fastapi.routing import APIRoute

from src.endpoints import auth_router, product_router, user_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(user_router)


routes = {}
for route in api_router.routes:
    if isinstance(route, APIRoute):
        resource = route.path.split("/")
        if len(resource) >= 4 and resource[3] not in routes:
            routes[resource[3]] = route.path
