"""
Module for the fastapi setup.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.config.core import core_settings
from src.endpoints import auth_router, product_router, user_router
from src.middlewares.exceptions import validation_request_exception_handler

app = FastAPI(root_path="/catalog_api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=core_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(exc_class_or_status_code=RequestValidationError, handler=validation_request_exception_handler)

app.include_router(
    router=auth_router,
    prefix="/authenthicate",
)
app.include_router(
    router=user_router,
    prefix="/users",
)
app.include_router(
    router=product_router,
    prefix="/products",
)

@app.get("/")
def read_root():
    """Root path."""
    return {"Message": "Ok"}
