from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import GenerationStatus
from app.schemas.common import IdCreatedAt


class GenerationRunCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"requested_solutions": 10, "seed": 123}]},
    )
    requested_solutions: int = Field(default=10, ge=1, le=200)
    seed: int | None = None


class GenerationRunOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "status": "completed",
                    "seed": 123,
                    "requested_solutions": 10,
                    "finished_at": "2025-01-01T00:00:01Z",
                    "error_message": None,
                }
            ]
        }
    )
    site_id: UUID
    status: GenerationStatus
    seed: int | None
    requested_solutions: int
    finished_at: datetime | None
    error_message: str | None


class PlanSolutionOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:01Z",
                    "run_id": "00000000-0000-0000-0000-000000000000",
                    "rank": 1,
                    "score": 0.95,
                    "metrics": {"network_total_length": None, "violations": 0},
                    "layout": {"placements": []},
                    "thumbnail_url": None,
                }
            ]
        }
    )
    run_id: UUID
    rank: int
    score: float
    metrics: dict[str, Any]
    layout: dict[str, Any]
    thumbnail_url: str | None
