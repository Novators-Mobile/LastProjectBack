from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.enums import AnalysisLayerType
from app.services.boundaries import get_boundary
from app.services.layers import upsert_layer


def run_analysis(db: Session, *, site_id) -> None:
    boundary = get_boundary(db, site_id)
    upsert_layer(
        db,
        site_id=site_id,
        layer_type=AnalysisLayerType.slope,
        payload={"status": "not_computed"},
    )
    upsert_layer(
        db,
        site_id=site_id,
        layer_type=AnalysisLayerType.buildable_areas,
        payload={"status": "computed", "areas": [boundary.geojson]},
    )
    upsert_layer(
        db,
        site_id=site_id,
        layer_type=AnalysisLayerType.infrastructure_nodes,
        payload={"status": "not_computed", "nodes": []},
    )
