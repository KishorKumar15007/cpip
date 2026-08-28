import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.orm import Session

from backend.api.dependencies import get_session
from backend.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.security.rate_limit import (
    check_login_rate_limit,
)
from backend.services.auth.service import AuthService


logger = logging.getLogger(__name__)


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
    request: Request,
    credentials: LoginRequest,
    session: Session = Depends(get_session),
):
    client_ip = request.client.host

    retry_after = check_login_rate_limit(
        client_ip,
    )

    if retry_after is not None:
        logger.warning(
            "Login rate limit exceeded for client IP %s",
            client_ip,
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
            headers={
                "Retry-After": str(retry_after),
            },
        )

    try:
        access_token, refresh_token = auth_service.login(
            session=session,
            email=credentials.email,
            password=credentials.password,
        )

    except ValueError as error:
        logger.warning(
            "Authentication failed for login attempt from client IP %s",
            client_ip,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    request: RefreshTokenRequest,
    session: Session = Depends(get_session),
):
    try:
        access_token, refresh_token = auth_service.refresh(
            session=session,
            refresh_token=request.refresh_token,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
