"""This module handles various exceptions."""
from datetime import UTC, datetime
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Global exception handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now(tz=UTC).isoformat()
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for Exception."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal Server error.",
            "error_type": exc.__class__.__name__,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "timestamp": datetime.now(tz=UTC).isoformat()
        },
    )


async def validation_request_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Customized exception for any Pydantic request validation errors as app exception handler."""
    errors = []

    for ex in exc.errors():

        message = ex.get("msg")
        field = ex.get("loc")[-1]
        err_type = ex.get("type")
        input_data = ex.get("input")

        if err_type == "missing":
            message = "This field is required."
        if err_type == "value_error":
            message = ex.get("ctx", {}).get("reason", message)

        err_data = {
            "message": message,
            "field": field,
            "input": input_data
        }
        errors.append(err_data)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Requested data missing.",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "details": errors
        }
    )

class ApiException(HTTPException):
    """Base HTTPException class."""
    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            message: str = "An unexpected error has occurred.",
            detail: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            ):
        err_detail = detail or {}
        err_detail.update(
            {
                "message": message,
                "error_code": status_code,
                "timestamp": datetime.now(tz=UTC).isoformat()
            }
        )

        super().__init__(status_code=status_code, detail=err_detail, headers=headers)


class NotFoundException(ApiException):
    """Resource not found exception."""
    def __init__(
            self,
            status_code: int = status.HTTP_404_NOT_FOUND,
            message: Optional[str] = "Not found.",
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None
            ):

        super().__init__(status_code=status_code, detail=detail, message=message, headers=headers)


class AlreadyExistException(ApiException):
    """Resource already exist exception."""
    def __init__(
            self,
            status_code: int = status.HTTP_409_CONFLICT,
            message: Optional[str] = "Resource already exist.",
            detail: Any = None,
            headers: Optional[Dict[str, Any]] = None
            ):

        super().__init__(status_code=status_code, detail=detail, message=message, headers=headers)
