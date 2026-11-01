from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import re

from app.core.config import settings
from app.core.database import get_db
from app.core.security import TOKEN_COOKIE, TOKEN_TTL_SECONDS, create_auth_token, hash_password, user_id_from_request, verify_password
from app.models.database import User

router = APIRouter(prefix="/api/auth", tags=["authentication"])


class Credentials(BaseModel):
    email: str = Field(min_length=5, max_length=320)
    password: str = Field(min_length=8, max_length=256)


def _email(value: str) -> str:
    value = value.strip().lower()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    return value


def _set_cookie(response: Response, user_id: str) -> None:
    response.set_cookie(
        TOKEN_COOKIE, create_auth_token(user_id), max_age=TOKEN_TTL_SECONDS,
        httponly=True, secure=settings.ENVIRONMENT.lower() not in {"development", "dev", "local"},
        samesite="lax", path="/",
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: Credentials, response: Response, db: AsyncSession = Depends(get_db)):
    email = _email(data.email)
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(email=email, password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    _set_cookie(response, user.id)
    return {"id": user.id, "email": user.email}


@router.post("/login")
async def login(data: Credentials, response: Response, db: AsyncSession = Depends(get_db)):
    email = _email(data.email)
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    _set_cookie(response, user.id)
    return {"id": user.id, "email": user.email}


@router.get("/me")
async def me(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = user_id_from_request(request)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    return {"id": user.id, "email": user.email}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(TOKEN_COOKIE, path="/", httponly=True, samesite="lax")
    return response
