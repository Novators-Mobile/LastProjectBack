from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from app.api.deps import AuthDep, DBSession
from app.db.session import SessionLocal
from app.schemas.generation import GenerationRunCreate, GenerationRunOut, PlanSolutionOut
from app.services.generation import (
    create_run,
    generate_solutions,
    get_run,
    list_runs,
    list_solutions,
)
from app.services.sites import get_site

router = APIRouter()


def _run_generation_task(site_id: UUID, run_id: UUID) -> None:
    db = SessionLocal()
    try:
        generate_solutions(db, site_id=site_id, run_id=run_id)
    finally:
        db.close()


@router.post(
    "/{site_id}/generation-runs",
    response_model=GenerationRunOut,
    status_code=202,
    summary="Запустить генерацию планов",
    description="Создаёт запуск генерации и запускает расчёт решений в фоне.",
)
def start_generation(
    site_id: UUID,
    payload: GenerationRunCreate,
    background_tasks: BackgroundTasks,
    db: DBSession,
    _: AuthDep,
) -> GenerationRunOut:
    get_site(db, site_id)
    run = create_run(
        db,
        site_id=site_id,
        requested_solutions=payload.requested_solutions,
        seed=payload.seed,
    )
    background_tasks.add_task(_run_generation_task, site_id, run.id)
    return GenerationRunOut.model_validate(run)


@router.get(
    "/{site_id}/generation-runs",
    response_model=list[GenerationRunOut],
    summary="Список запусков генерации",
    description="Возвращает историю запусков генерации для площадки.",
)
def list_generation_runs(site_id: UUID, db: DBSession, _: AuthDep) -> list[GenerationRunOut]:
    get_site(db, site_id)
    runs = list_runs(db, site_id=site_id)
    return [GenerationRunOut.model_validate(r) for r in runs]


@router.get(
    "/{site_id}/generation-runs/{run_id}",
    response_model=GenerationRunOut,
    summary="Получить запуск генерации",
    description="Возвращает состояние запуска генерации.",
)
def get_generation_run(site_id: UUID, run_id: UUID, db: DBSession, _: AuthDep) -> GenerationRunOut:
    get_site(db, site_id)
    run = get_run(db, site_id=site_id, run_id=run_id)
    return GenerationRunOut.model_validate(run)


@router.get(
    "/{site_id}/generation-runs/{run_id}/solutions",
    response_model=list[PlanSolutionOut],
    summary="Получить решения запуска",
    description="Возвращает решения (планы) для запуска генерации, отсортированные по рангу.",
)
def get_generation_solutions(
    site_id: UUID,
    run_id: UUID,
    db: DBSession,
    _: AuthDep,
) -> list[PlanSolutionOut]:
    get_site(db, site_id)
    run = get_run(db, site_id=site_id, run_id=run_id)
    sols = list_solutions(db, run_id=run.id)
    return [PlanSolutionOut.model_validate(s) for s in sols]
