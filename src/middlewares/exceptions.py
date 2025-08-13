from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


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
