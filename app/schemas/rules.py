from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import OptimizationRuleType
from app.schemas.common import IdCreatedAt


class RuleCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "rule_type": "near",
                    "source_object_id": None,
                    "target_object_id": None,
                    "weight": 1.0,
                    "params": {"max_distance_m": 50},
                },
                {"rule_type": "minimize_network_length", "weight": 1.0, "params": {}},
            ]
        }
    )
    rule_type: OptimizationRuleType
    source_object_id: UUID | None = None
    target_object_id: UUID | None = None
    weight: float = Field(default=1.0, gt=0)
    params: dict[str, Any] = Field(default_factory=dict)


class RuleOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "rule_type": "minimize_network_length",
                    "source_object_id": None,
                    "target_object_id": None,
                    "weight": 1.0,
                    "params": {},
                }
            ]
        }
    )
    site_id: UUID
    rule_type: OptimizationRuleType
    source_object_id: UUID | None
    target_object_id: UUID | None
    weight: float
    params: dict[str, Any]
