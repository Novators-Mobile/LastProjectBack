from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import IdCreatedAt
from app.schemas.generation import GenerationRunOut
from app.schemas.uploads import UploadOut


class SiteCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"name": "Площадка №1"}]},
    )
    name: str = Field(min_length=1, max_length=200)


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)


class SiteOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "name": "Площадка №1",
                }
            ]
        }
    )
    name: str


class BoundaryUpsert(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "geojson": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
                    }
                }
            ]
        }
    )
    geojson: dict[str, Any]


class BoundaryOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "geojson": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
                    },
                }
            ]
        }
    )
    site_id: UUID
    geojson: dict[str, Any]


class SiteSummaryOut(BaseModel):
    site: SiteOut
    boundary_present: bool
    uploads: dict[str, int]
    analysis: dict[str, Any]
    last_generation_run: GenerationRunOut | None
    solutions_count: int


class SiteCreateWithUploadsOut(BaseModel):
    site: SiteOut
    uploads: list[UploadOut]
