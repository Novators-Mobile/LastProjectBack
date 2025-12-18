from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import AppError
from app.db.session import get_db


def require_auth(authorization: str | None = Header(default=None)) -> None:
    if settings.auth_disabled:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError("Не авторизован", status_code=401)
    token = authorization.removeprefix("Bearer ").strip()
    if token != settings.access_token:
        raise AppError("Не авторизован", status_code=401)


DBSession = Annotated[Session, Depends(get_db)]
AuthDep = Annotated[None, Depends(require_auth)]
