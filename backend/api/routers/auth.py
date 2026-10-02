import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from sqlalchemy.orm import Session

from backend.api.dependencies import get_session
from backend.schemas.auth import (
    FinalizeRegistrationRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.security.rate_limit import (
    check_login_rate_limit,
)
from backend.services.auth.service import AuthService
import os
from backend.services.auth.service import REGISTRATION_STATE_SECONDS


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()
REFRESH_COOKIE = "cpip_refresh_token"
REGISTRATION_COOKIE = "cpip_registration"


def set_refresh_cookie(request: Request, response: Response, token: str) -> None:
    response.set_cookie(REFRESH_COOKIE, token, httponly=True, secure=request.url.scheme == "https", samesite="lax", max_age=60 * 60 * 24 * int(os.environ["REFRESH_TOKEN_EXPIRE_DAYS"]), path="/api/auth")


def set_registration_cookie(request: Request, response: Response, token: str) -> None:
    response.set_cookie(REGISTRATION_COOKIE, token, httponly=True, secure=request.url.scheme == "https", samesite="lax", max_age=REGISTRATION_STATE_SECONDS, path="/api/auth")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: Request,
    payload: RegisterRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    try:
        registration_id = auth_service.begin_registration(session, payload.email, payload.password)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )

    set_registration_cookie(request, response, registration_id)
    return {"status": "registration_started"}


@router.post("/register/finalize", response_model=TokenResponse)
def finalize_registration(request: Request, payload: FinalizeRegistrationRequest, response: Response, session: Session = Depends(get_session)):
    try:
        _, access_token, refresh_token = auth_service.finalize_registration(session, request.cookies.get(REGISTRATION_COOKIE, ""), payload.username)
    except ValueError as error:
        detail = str(error)
        code = status.HTTP_409_CONFLICT if detail in {"Email already exists.", "Username unavailable."} else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=detail)
    response.delete_cookie(REGISTRATION_COOKIE, path="/api/auth")
    set_refresh_cookie(request, response, refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: Request,
    response: Response,
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

    set_refresh_cookie(request, response, refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    request: Request,
    payload: RefreshTokenRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    refresh_token = payload.refresh_token or request.cookies.get(REFRESH_COOKIE)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh session is missing.")
    try:
        access_token, refresh_token = auth_service.refresh(
            session=session,
            refresh_token=refresh_token,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    set_refresh_cookie(request, response, refresh_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, session: Session = Depends(get_session)):
    refresh_token = request.cookies.get(REFRESH_COOKIE)
    if refresh_token:
        auth_service.revoke_refresh_token(session, refresh_token)
    response.delete_cookie(REFRESH_COOKIE, path="/api/auth")
