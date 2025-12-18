from __future__ import annotations

import uuid

from sqlalchemy import JSON, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class OptimizationRule(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "optimization_rules"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )
    rule_type: Mapped[str] = mapped_column(nullable=False)
    source_object_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("planned_objects.id", ondelete="SET NULL"),
        nullable=True,
    )
    target_object_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("planned_objects.id", ondelete="SET NULL"),
        nullable=True,
    )
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    params: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
