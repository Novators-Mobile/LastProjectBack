from __future__ import annotations

import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class RestrictionZone(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "restriction_zones"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )
    zone_type: Mapped[str] = mapped_column(String(120), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="forbidden", nullable=False)
    geometry: Mapped[dict] = mapped_column(JSON, nullable=False)
