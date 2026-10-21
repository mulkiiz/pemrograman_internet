"""Hash password, membuat JWT, dan memeriksa identitas serta peran."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import Session

import crud
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from database import get_session
from models import User

password_hasher = PasswordHash.recommended()
# Skema pertama: Swagger meminta username/password dan mengambil token sendiri.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
# Skema kedua: mahasiswa dapat menempel token hasil POST /auth/token secara manual.
manual_bearer_scheme = HTTPBearer(
    scheme_name="ManualBearerToken",
    description="Tempel nilai access_token dari POST /auth/token tanpa awalan 'Bearer '.",
    auto_error=False,
)


def hash_password(password: str) -> str:
    """Simpan hash, bukan password asli."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(username: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "exp": expires_at}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    # Parameter versi lama: token: Annotated[str, Depends(oauth2_scheme)]
    oauth2_token: Annotated[str | None, Depends(oauth2_scheme)],
    manual_credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(manual_bearer_scheme)
    ],
    session: Session = Depends(get_session),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau sudah kedaluwarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = oauth2_token or (
        manual_credentials.credentials if manual_credentials is not None else None
    )
    if token is None:
        raise credentials_error

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not isinstance(username, str):
            raise credentials_error
    except InvalidTokenError as exc:
        raise credentials_error from exc

    user = crud.get_user_by_username(session, username)
    if user is None or not user.is_active:
        raise credentials_error
    return user


def require_roles(*allowed_roles: str):
    """Dependency untuk membatasi endpoint menurut role pengguna."""
    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role Anda tidak diizinkan mengakses fitur ini",
            )
        return current_user

    return role_checker
