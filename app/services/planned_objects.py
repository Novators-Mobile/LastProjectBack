from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.planned_object import PlannedObject


def create_planned_object(db: Session, *, site_id, data) -> PlannedObject:
    if "object_type" in data and hasattr(data["object_type"], "value"):
        data["object_type"] = data["object_type"].value
    obj = PlannedObject(site_id=site_id, **data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_planned_objects(db: Session, site_id) -> list[PlannedObject]:
    return db.query(PlannedObject).filter(PlannedObject.site_id == site_id).all()
