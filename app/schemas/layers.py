from __future__ import annotations

from typing import Any
from uuid import UUID

from app.models.enums import AnalysisLayerType
from app.schemas.common import IdCreatedAt


class AnalysisLayerOut(IdCreatedAt):
    site_id: UUID
    layer_type: AnalysisLayerType
    payload: dict[str, Any]

