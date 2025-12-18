from __future__ import annotations

import uuid

from sqlalchemy import JSON, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PlanSolution(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "plan_solutions"

    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("generation_runs.id", ondelete="CASCADE"),
        index=True,
    )
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    layout: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
