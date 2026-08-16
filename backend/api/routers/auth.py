from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.dependencies import get_session
from backend.schemas.auth import RegisterRequest
from backend.services.auth.service import AuthService
from backend.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
):
    try:
        user = auth_service.register(
            session=session,
            username=request.username,
            email=request.email,
            password=request.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )

    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
    }

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
):
    try:
        access_token = auth_service.login(
            session=session,
            email=request.email,
            password=request.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
