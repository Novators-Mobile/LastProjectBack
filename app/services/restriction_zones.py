from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.restriction_zone import RestrictionZone


def create_zone(
    db: Session,
    *,
    site_id,
    zone_type: str,
    severity,
    geometry: dict,
) -> RestrictionZone:
    zone = RestrictionZone(
        site_id=site_id,
        zone_type=zone_type,
        severity=getattr(severity, "value", severity),
        geometry=geometry,
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def list_zones(db: Session, site_id) -> list[RestrictionZone]:
    return db.query(RestrictionZone).filter(RestrictionZone.site_id == site_id).all()


def delete_zone(db: Session, *, site_id, zone_id) -> None:
    zone = (
        db.query(RestrictionZone)
        .filter(RestrictionZone.site_id == site_id, RestrictionZone.id == zone_id)
        .first()
    )
    if not zone:
        raise AppError("Зона ограничений не найдена", status_code=404)
    db.delete(zone)
    db.commit()


def update_zone(
    db: Session,
    *,
    site_id,
    zone_id,
    zone_type: str | None,
    severity,
    geometry: dict | None,
) -> RestrictionZone:
    zone = (
        db.query(RestrictionZone)
        .filter(RestrictionZone.site_id == site_id, RestrictionZone.id == zone_id)
        .first()
    )
    if not zone:
        raise AppError("Зона ограничений не найдена", status_code=404)

    if zone_type is not None:
        zone.zone_type = zone_type
    if severity is not None:
        zone.severity = getattr(severity, "value", severity)
    if geometry is not None:
        zone.geometry = geometry
    db.commit()
    db.refresh(zone)
    return zone
