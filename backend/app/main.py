from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from jwt import ExpiredSignatureError, InvalidTokenError

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas import LoginRequest, TokenRefreshRequest, TokenResponse

app = FastAPI(
    title="FastAPI JWT Demo",
    version="0.1.0",
    description="Web API con autenticacion JWT y refresh token.",
)

_FRONTEND_INDEX = Path(__file__).resolve().parent / "static" / "index.html"


@app.get("/", include_in_schema=False)
def welcome_page() -> FileResponse:
    """Serve the static welcome frontend and return 503 if file is unavailable."""
    if not _FRONTEND_INDEX.is_file():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La página de bienvenida no está disponible temporalmente",
        )
    return FileResponse(_FRONTEND_INDEX)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/token", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    user = authenticate_user(credentials.username, credentials.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    return TokenResponse(
        access_token=create_access_token(user.username),
        refresh_token=create_refresh_token(user.username),
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(payload: TokenRefreshRequest) -> TokenResponse:
    try:
        token_payload = decode_token(payload.refresh_token)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado",
        ) from exc
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalido",
        ) from exc

    if token_payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token enviado no es un refresh token",
        )

    subject = token_payload.get("sub")
    if subject != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado",
        )

    return TokenResponse(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
