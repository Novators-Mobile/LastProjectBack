from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import RestrictionSeverity
from app.schemas.common import IdCreatedAt


class RestrictionZoneCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "zone_type": "СЗЗ",
                    "severity": "forbidden",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]],
                    },
                }
            ]
        }
    )
    zone_type: str = Field(min_length=1, max_length=120)
    severity: RestrictionSeverity = RestrictionSeverity.forbidden
    geometry: dict[str, Any]


class RestrictionZoneUpdate(BaseModel):
    zone_type: str | None = Field(default=None, min_length=1, max_length=120)
    severity: RestrictionSeverity | None = None
    geometry: dict[str, Any] | None = None


class RestrictionZoneOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "zone_type": "СЗЗ",
                    "severity": "forbidden",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]],
                    },
                }
            ]
        }
    )
    site_id: UUID
    zone_type: str
    severity: RestrictionSeverity
    geometry: dict[str, Any]
