from __future__ import annotations

import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ExistingFeature(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "existing_features"

    site_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sites.id", ondelete="CASCADE"),
        index=True,
    )
    feature_type: Mapped[str] = mapped_column(nullable=False)
    geometry: Mapped[dict] = mapped_column(JSON, nullable=False)
    properties: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
