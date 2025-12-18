from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import PlannedObjectType
from app.schemas.common import IdCreatedAt


class PlannedObjectCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "object_type": "warehouse",
                    "template_key": "warehouse_raw_materials",
                    "name": "Склад сырья",
                    "length_min": 100,
                    "length_max": 200,
                    "width_min": 48,
                    "width_max": 96,
                    "height_min": 10,
                    "height_max": 12,
                }
            ]
        }
    )
    object_type: PlannedObjectType
    template_key: str | None = Field(default=None, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    length_min: float | None = None
    length_max: float | None = None
    width_min: float | None = None
    width_max: float | None = None
    height_min: float | None = None
    height_max: float | None = None

    @model_validator(mode="after")
    def validate_ranges(self) -> PlannedObjectCreate:
        pairs = [
            ("length_min", "length_max"),
            ("width_min", "width_max"),
            ("height_min", "height_max"),
        ]
        for mn, mx in pairs:
            vmin = getattr(self, mn)
            vmax = getattr(self, mx)
            if vmin is not None and vmax is not None and vmin > vmax:
                raise ValueError(f"{mn} должен быть меньше или равен {mx}")
        return self


class PlannedObjectOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "object_type": "warehouse",
                    "template_key": "warehouse_raw_materials",
                    "name": "Склад сырья",
                    "length_min": 100,
                    "length_max": 200,
                    "width_min": 48,
                    "width_max": 96,
                    "height_min": 10,
                    "height_max": 12,
                }
            ]
        }
    )
    site_id: UUID
    object_type: PlannedObjectType
    template_key: str | None
    name: str
    length_min: float | None
    length_max: float | None
    width_min: float | None
    width_max: float | None
    height_min: float | None
    height_max: float | None
