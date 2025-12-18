from __future__ import annotations

import random
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.enums import AnalysisLayerType, GenerationStatus
from app.models.generation_run import GenerationRun
from app.models.plan_solution import PlanSolution
from app.models.planned_object import PlannedObject
from app.services.geojson import geojson_bbox
from app.services.layers import list_layers


def create_run(
    db: Session,
    *,
    site_id,
    requested_solutions: int,
    seed: int | None,
) -> GenerationRun:
    run = GenerationRun(site_id=site_id, requested_solutions=requested_solutions, seed=seed)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_run(db: Session, *, site_id, run_id) -> GenerationRun:
    run = (
        db.query(GenerationRun)
        .filter(GenerationRun.site_id == site_id, GenerationRun.id == run_id)
        .first()
    )
    if not run:
        raise AppError("Запуск генерации не найден", status_code=404)
    return run


def list_runs(db: Session, *, site_id) -> list[GenerationRun]:
    return (
        db.query(GenerationRun)
        .filter(GenerationRun.site_id == site_id)
        .order_by(GenerationRun.created_at.desc())
        .all()
    )


def list_solutions(db: Session, *, run_id) -> list[PlanSolution]:
    return (
        db.query(PlanSolution)
        .filter(PlanSolution.run_id == run_id)
        .order_by(PlanSolution.rank.asc())
        .all()
    )


def _get_buildable_bbox(db: Session, *, site_id) -> tuple[float, float, float, float]:
    layers = list_layers(db, site_id)
    buildable = next(
        (layer for layer in layers if layer.layer_type == AnalysisLayerType.buildable_areas.value),
        None,
    )
    if not buildable:
        raise AppError("Нет слоя пятен застройки. Сначала запустите анализ.", status_code=409)
    areas = buildable.payload.get("areas") if isinstance(buildable.payload, dict) else None
    if not areas:
        raise AppError("Слой пятен застройки пуст. Сначала запустите анализ.", status_code=409)
    return geojson_bbox(areas[0])


def generate_solutions(db: Session, *, site_id, run_id) -> None:
    run = get_run(db, site_id=site_id, run_id=run_id)
    if run.status not in (GenerationStatus.queued.value, GenerationStatus.failed.value):
        return

    run.status = GenerationStatus.running.value
    db.commit()

    try:
        rng = random.Random(run.seed)
        min_x, min_y, max_x, max_y = _get_buildable_bbox(db, site_id=site_id)
        objects = db.query(PlannedObject).filter(PlannedObject.site_id == site_id).all()

        solutions: list[PlanSolution] = []
        for rank in range(1, run.requested_solutions + 1):
            placements = []
            for obj in objects:
                x = rng.uniform(min_x, max_x)
                y = rng.uniform(min_y, max_y)
                placements.append(
                    {
                        "planned_object_id": str(obj.id),
                        "name": obj.name,
                        "object_type": obj.object_type,
                        "position": {"x": x, "y": y},
                    }
                )
            score = rng.random()
            solutions.append(
                PlanSolution(
                    run_id=run.id,
                    rank=rank,
                    score=score,
                    metrics={"network_total_length": None, "violations": 0},
                    layout={"placements": placements},
                )
            )
        for s in solutions:
            db.add(s)

        run.status = GenerationStatus.completed.value
        run.finished_at = datetime.now(UTC)
        db.commit()
    except Exception as exc:
        run.status = GenerationStatus.failed.value
        run.error_message = str(exc)
        run.finished_at = datetime.now(UTC)
        db.commit()
        raise
