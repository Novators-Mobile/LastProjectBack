from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.site_boundary import SiteBoundary


def upsert_boundary(db: Session, *, site_id, geojson: dict) -> SiteBoundary:
    boundary = db.query(SiteBoundary).filter(SiteBoundary.site_id == site_id).first()
    if boundary:
        boundary.geojson = geojson
    else:
        boundary = SiteBoundary(site_id=site_id, geojson=geojson)
        db.add(boundary)
    db.commit()
    db.refresh(boundary)
    return boundary


def get_boundary(db: Session, site_id) -> SiteBoundary:
    boundary = db.query(SiteBoundary).filter(SiteBoundary.site_id == site_id).first()
    if not boundary:
        raise AppError("Граница площадки не найдена", status_code=404)
    return boundary
