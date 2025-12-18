from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.analysis_layer import AnalysisLayer
from app.models.enums import AnalysisLayerType, UploadType
from app.models.generation_run import GenerationRun
from app.models.plan_solution import PlanSolution
from app.models.planned_object import PlannedObject
from app.models.restriction_zone import RestrictionZone
from app.models.rule import OptimizationRule
from app.models.site import Site
from app.models.site_boundary import SiteBoundary
from app.models.upload import Upload


def create_site(db: Session, *, name: str) -> Site:
    site = Site(name=name)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


def list_sites(db: Session) -> list[Site]:
    return db.query(Site).order_by(Site.created_at.desc()).all()


def get_site(db: Session, site_id) -> Site:
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise AppError("Площадка не найдена", status_code=404)
    return site


def update_site(db: Session, *, site_id, name: str | None) -> Site:
    site = get_site(db, site_id)
    if name is not None:
        site.name = name
    db.commit()
    db.refresh(site)
    return site


def delete_site(db: Session, *, site_id) -> None:
    site = get_site(db, site_id)
    run_ids = [
        r[0] for r in db.query(GenerationRun.id).filter(GenerationRun.site_id == site_id).all()
    ]
    if run_ids:
        db.query(PlanSolution).filter(PlanSolution.run_id.in_(run_ids)).delete(
            synchronize_session=False
        )
    db.query(GenerationRun).filter(GenerationRun.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(OptimizationRule).filter(OptimizationRule.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(PlannedObject).filter(PlannedObject.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(RestrictionZone).filter(RestrictionZone.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(AnalysisLayer).filter(AnalysisLayer.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(SiteBoundary).filter(SiteBoundary.site_id == site_id).delete(
        synchronize_session=False
    )
    db.query(Upload).filter(Upload.site_id == site_id).delete(synchronize_session=False)

    db.delete(site)
    db.commit()


def get_site_summary(db: Session, *, site_id) -> dict:
    site = get_site(db, site_id)

    boundary_present = (
        db.query(SiteBoundary.id).filter(SiteBoundary.site_id == site_id).first() is not None
    )

    uploads_rows = (
        db.query(Upload.upload_type, func.count(Upload.id))
        .filter(Upload.site_id == site_id)
        .group_by(Upload.upload_type)
        .all()
    )
    uploads: dict[str, int] = {row[0]: int(row[1]) for row in uploads_rows}
    for t in (UploadType.boundary.value, UploadType.terrain.value, UploadType.existing.value):
        uploads.setdefault(t, 0)

    layers = db.query(AnalysisLayer).filter(AnalysisLayer.site_id == site_id).all()
    analysis: dict[str, dict] = {}
    for t in (
        AnalysisLayerType.slope.value,
        AnalysisLayerType.buildable_areas.value,
        AnalysisLayerType.infrastructure_nodes.value,
    ):
        layer = next((layer_item for layer_item in layers if layer_item.layer_type == t), None)
        if not layer:
            analysis[t] = {"present": False, "status": None}
            continue
        status = layer.payload.get("status") if isinstance(layer.payload, dict) else None
        analysis[t] = {"present": True, "status": status}

    last_run = (
        db.query(GenerationRun)
        .filter(GenerationRun.site_id == site_id)
        .order_by(GenerationRun.created_at.desc())
        .first()
    )
    if last_run:
        solutions_count = (
            db.query(func.count(PlanSolution.id))
            .filter(PlanSolution.run_id == last_run.id)
            .scalar()
        )
        solutions_count = int(solutions_count or 0)
    else:
        solutions_count = 0

    return {
        "site": site,
        "boundary_present": boundary_present,
        "uploads": uploads,
        "analysis": analysis,
        "last_generation_run": last_run,
        "solutions_count": solutions_count,
    }
