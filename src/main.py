"""
Module for the fastapi setup.
"""

from typing import Any, Dict

from fastapi import FastAPI, responses, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.config.core import core_settings
from src.middlewares.exceptions import validation_request_exception_handler
from src.routers import api_router, routes

app = FastAPI(root_path="/catalog_api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=core_settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(exc_class_or_status_code=RequestValidationError, handler=validation_request_exception_handler)
app.include_router(api_router)


@app.get("/")
def root_endpoint() -> Dict[str, Any]:
    """Root endpoint."""
    return responses.JSONResponse(
        content={
            "message": "Ok",
            "routes": routes,
        },
        status_code=status.HTTP_200_OK
    )
