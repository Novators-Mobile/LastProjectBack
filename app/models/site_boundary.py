from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.site import Site


class SiteBoundary(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "site_boundaries"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        unique=True,
    )
    geojson: Mapped[dict] = mapped_column(JSON, nullable=False)

    site: Mapped[Site] = relationship(back_populates="boundary")
