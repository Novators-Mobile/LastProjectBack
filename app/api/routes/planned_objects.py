from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AuthDep, DBSession
from app.schemas.planned_objects import PlannedObjectCreate, PlannedObjectOut
from app.services.planned_objects import create_planned_object, list_planned_objects
from app.services.sites import get_site

router = APIRouter()


@router.post(
    "/{site_id}/planned-objects",
    response_model=PlannedObjectOut,
    summary="Создать объект",
    description="Создаёт объект (здание/цех/склад/сеть) с диапазонами параметров.",
)
def create_object(
    site_id: UUID,
    payload: PlannedObjectCreate,
    db: DBSession,
    _: AuthDep,
) -> PlannedObjectOut:
    get_site(db, site_id)
    obj = create_planned_object(db, site_id=site_id, data=payload.model_dump())
    return PlannedObjectOut.model_validate(obj)


@router.get(
    "/{site_id}/planned-objects",
    response_model=list[PlannedObjectOut],
    summary="Список объектов",
    description="Возвращает список объектов производственной схемы для площадки.",
)
def list_objects(site_id: UUID, db: DBSession, _: AuthDep) -> list[PlannedObjectOut]:
    get_site(db, site_id)
    objs = list_planned_objects(db, site_id)
    return [PlannedObjectOut.model_validate(o) for o in objs]
