from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PlannedObject(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "planned_objects"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )
    object_type: Mapped[str] = mapped_column(String(50), nullable=False)
    template_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    length_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    length_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    width_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    width_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    height_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    height_max: Mapped[float | None] = mapped_column(Float, nullable=True)
