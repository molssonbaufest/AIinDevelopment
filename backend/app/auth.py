from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 3600
ALGORITHM = "HS256"
SECRET_KEY = "change-this-in-production"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class AuthenticatedUser:
    username: str
    hashed_password: str


_DEMO_USER = AuthenticatedUser(
    username="admin",
    hashed_password=pwd_context.hash("admin123"),
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> AuthenticatedUser | None:
    if username != _DEMO_USER.username:
        return None
    if not verify_password(password, _DEMO_USER.hashed_password):
        return None
    return _DEMO_USER


def _build_token(subject: str, expires_in: int, token_type: str) -> str:
    issued_at = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(issued_at.timestamp()),
        "exp": int((issued_at + timedelta(seconds=expires_in)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(subject: str) -> str:
    return _build_token(subject=subject, expires_in=ACCESS_TOKEN_EXPIRE_SECONDS, token_type="access")


def create_refresh_token(subject: str) -> str:
    return _build_token(subject=subject, expires_in=REFRESH_TOKEN_EXPIRE_SECONDS, token_type="refresh")


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
