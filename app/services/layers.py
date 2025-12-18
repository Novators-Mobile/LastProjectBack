from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.analysis_layer import AnalysisLayer
from app.models.enums import AnalysisLayerType


def list_layers(db: Session, site_id) -> list[AnalysisLayer]:
    return db.query(AnalysisLayer).filter(AnalysisLayer.site_id == site_id).all()


def upsert_layer(
    db: Session,
    *,
    site_id,
    layer_type: AnalysisLayerType,
    payload: dict,
) -> AnalysisLayer:
    layer = (
        db.query(AnalysisLayer)
        .filter(AnalysisLayer.site_id == site_id, AnalysisLayer.layer_type == layer_type.value)
        .first()
    )
    if layer:
        layer.payload = payload
    else:
        layer = AnalysisLayer(site_id=site_id, layer_type=layer_type.value, payload=payload)
        db.add(layer)
    db.commit()
    db.refresh(layer)
    return layer
