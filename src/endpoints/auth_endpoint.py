"""This module handle auth endpoint."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.db import get_db
from src.schemas import TokenResponse, UserAuthSchema
from src.services.auth import generate_token


router = APIRouter(
    prefix="/authenthicate",
    tags=["Auth"]
)


@router.post('/', description='User authentication.', response_model=TokenResponse)
async def login_for_access_token(authenticate: UserAuthSchema, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Returns The generated access token."""
    try:
        access_token = await generate_token(db=db, email=authenticate.email, password=authenticate.password)
        return TokenResponse(access_token=access_token, token_type="bearer")

    except HTTPException as http_ex:
        raise http_ex
    except Exception as exc:
        print(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error has occurred.",
        ) from exc

auth_router = router
