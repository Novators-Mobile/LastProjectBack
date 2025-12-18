from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AuthDep, DBSession
from app.schemas.restriction_zones import (
    RestrictionZoneCreate,
    RestrictionZoneOut,
    RestrictionZoneUpdate,
)
from app.services.restriction_zones import create_zone, delete_zone, list_zones, update_zone
from app.services.sites import get_site

router = APIRouter()


@router.post(
    "/{site_id}/restriction-zones",
    response_model=RestrictionZoneOut,
    summary="Создать зону ограничений",
    description="Создаёт зону с особыми условиями (запрет/ограничение) в виде GeoJSON-полигона.",
)
def create_zone_endpoint(
    site_id: UUID,
    payload: RestrictionZoneCreate,
    db: DBSession,
    _: AuthDep,
) -> RestrictionZoneOut:
    get_site(db, site_id)
    zone = create_zone(
        db,
        site_id=site_id,
        zone_type=payload.zone_type,
        severity=payload.severity,
        geometry=payload.geometry,
    )
    return RestrictionZoneOut.model_validate(zone)


@router.get(
    "/{site_id}/restriction-zones",
    response_model=list[RestrictionZoneOut],
    summary="Список зон ограничений",
    description="Возвращает все зоны ограничений для площадки.",
)
def list_zones_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> list[RestrictionZoneOut]:
    get_site(db, site_id)
    zones = list_zones(db, site_id)
    return [RestrictionZoneOut.model_validate(z) for z in zones]


@router.delete(
    "/{site_id}/restriction-zones/{zone_id}",
    status_code=204,
    summary="Удалить зону ограничений",
    description="Удаляет зону ограничений по `zone_id`.",
)
def delete_zone_endpoint(site_id: UUID, zone_id: UUID, db: DBSession, _: AuthDep) -> None:
    get_site(db, site_id)
    delete_zone(db, site_id=site_id, zone_id=zone_id)


@router.put(
    "/{site_id}/restriction-zones/{zone_id}",
    response_model=RestrictionZoneOut,
    summary="Обновить зону ограничений",
    description="Обновляет тип/строгость/геометрию зоны ограничений.",
)
def update_zone_endpoint(
    site_id: UUID,
    zone_id: UUID,
    payload: RestrictionZoneUpdate,
    db: DBSession,
    _: AuthDep,
) -> RestrictionZoneOut:
    get_site(db, site_id)
    zone = update_zone(
        db,
        site_id=site_id,
        zone_id=zone_id,
        zone_type=payload.zone_type,
        severity=payload.severity,
        geometry=payload.geometry,
    )
    return RestrictionZoneOut.model_validate(zone)
