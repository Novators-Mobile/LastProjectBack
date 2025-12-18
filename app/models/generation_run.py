from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class GenerationRun(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "generation_runs"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[str] = mapped_column(default="queued", nullable=False)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    requested_solutions: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
