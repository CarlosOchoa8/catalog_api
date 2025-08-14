"""Authentication endpoints module."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.db import get_db
from src.schemas import TokenResponse, UserAuthSchema
from src.services.auth import generate_token

router = APIRouter()


@router.post('/', description='User authentication.', response_model=TokenResponse)
async def login_for_access_token(authenticate: UserAuthSchema, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Returns The generated access token."""
    access_token = generate_token(db=db, email=authenticate.email, password=authenticate.password)
    return TokenResponse(access_token=access_token, token_type="bearer")

auth_router = router
