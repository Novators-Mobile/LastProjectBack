from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.site_boundary import SiteBoundary


class Site(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "sites"

    name: Mapped[str] = mapped_column(String(200), nullable=False)

    boundary: Mapped[SiteBoundary | None] = relationship(back_populates="site", uselist=False)
