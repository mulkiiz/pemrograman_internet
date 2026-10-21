"""Endpoint login OAuth2 password flow dan informasi pengguna aktif."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

import crud
from database import get_session
from models import User
from schemas import Token, UserPublic
from security import create_access_token, get_current_user, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = crud.get_user_by_username(session, form.username)
    if (
        user is None
        or not user.is_active
        or not verify_password(form.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.username))


@router.get("/me", response_model=UserPublic)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
