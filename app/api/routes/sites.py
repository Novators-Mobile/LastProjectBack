from uuid import UUID

from fastapi import APIRouter, File, Form, UploadFile

from app.api.deps import AuthDep, DBSession
from app.models.enums import UploadType
from app.schemas.generation import GenerationRunOut
from app.schemas.sites import (
    BoundaryOut,
    BoundaryUpsert,
    SiteCreate,
    SiteCreateWithUploadsOut,
    SiteOut,
    SiteSummaryOut,
    SiteUpdate,
)
from app.schemas.uploads import UploadOut
from app.services.boundaries import get_boundary, upsert_boundary
from app.services.sites import (
    create_site,
    delete_site,
    get_site,
    get_site_summary,
    list_sites,
    update_site,
)
from app.services.uploads import save_upload

router = APIRouter()

required_upload_file = File(...)
optional_upload_file = File(default=None)


@router.post(
    "",
    response_model=SiteOut,
    summary="Создать площадку",
    description="Создаёт новую площадку.",
)
def create_site_endpoint(payload: SiteCreate, db: DBSession, _: AuthDep) -> SiteOut:
    site = create_site(db, name=payload.name)
    return SiteOut.model_validate(site)


@router.post(
    "/with-uploads",
    response_model=SiteCreateWithUploadsOut,
    status_code=201,
    summary="Создать площадку с файлами",
    description="Создаёт площадку и сохраняет загруженные файлы в хранилище.",
)
def create_site_with_uploads_endpoint(
    db: DBSession,
    _: AuthDep,
    name: str = Form(...),
    boundary_file: UploadFile = required_upload_file,
    terrain_file: UploadFile = required_upload_file,
    existing_file: UploadFile | None = optional_upload_file,
) -> SiteCreateWithUploadsOut:
    site = create_site(db, name=name)
    uploads = [
        save_upload(db, site_id=site.id, upload_type=UploadType.boundary, file=boundary_file),
        save_upload(db, site_id=site.id, upload_type=UploadType.terrain, file=terrain_file),
    ]
    if existing_file is not None:
        uploads.append(
            save_upload(db, site_id=site.id, upload_type=UploadType.existing, file=existing_file)
        )
    return SiteCreateWithUploadsOut(
        site=SiteOut.model_validate(site),
        uploads=[UploadOut.model_validate(u) for u in uploads],
    )


@router.get(
    "",
    response_model=list[SiteOut],
    summary="Список площадок",
    description="Возвращает список площадок.",
)
def list_sites_endpoint(db: DBSession, _: AuthDep) -> list[SiteOut]:
    sites = list_sites(db)
    return [SiteOut.model_validate(s) for s in sites]


@router.get(
    "/{site_id}",
    response_model=SiteOut,
    summary="Получить площадку",
    description="Возвращает площадку по `site_id`.",
)
def get_site_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> SiteOut:
    site = get_site(db, site_id)
    return SiteOut.model_validate(site)


@router.patch(
    "/{site_id}",
    response_model=SiteOut,
    summary="Обновить площадку",
    description="Обновляет поля площадки (например, имя).",
)
def update_site_endpoint(
    site_id: UUID,
    payload: SiteUpdate,
    db: DBSession,
    _: AuthDep,
) -> SiteOut:
    site = update_site(db, site_id=site_id, name=payload.name)
    return SiteOut.model_validate(site)


@router.delete(
    "/{site_id}",
    status_code=204,
    summary="Удалить площадку",
    description="Удаляет площадку и связанные данные.",
)
def delete_site_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> None:
    delete_site(db, site_id=site_id)


@router.get(
    "/{site_id}/summary",
    response_model=SiteSummaryOut,
    summary="Сводка по площадке",
    description="Возвращает статусы загрузок, анализа и генерации для площадки.",
)
def get_site_summary_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> SiteSummaryOut:
    summary = get_site_summary(db, site_id=site_id)
    last_run = summary["last_generation_run"]
    return SiteSummaryOut(
        site=SiteOut.model_validate(summary["site"]),
        boundary_present=bool(summary["boundary_present"]),
        uploads=dict(summary["uploads"]),
        analysis=dict(summary["analysis"]),
        last_generation_run=GenerationRunOut.model_validate(last_run) if last_run else None,
        solutions_count=int(summary["solutions_count"]),
    )


@router.put(
    "/{site_id}/boundary",
    response_model=BoundaryOut,
    summary="Задать границу площадки",
    description="Создаёт или обновляет геометрию границы площадки в формате GeoJSON.",
)
def upsert_boundary_endpoint(
    site_id: UUID,
    payload: BoundaryUpsert,
    db: DBSession,
    _: AuthDep,
) -> BoundaryOut:
    get_site(db, site_id)
    boundary = upsert_boundary(db, site_id=site_id, geojson=payload.geojson)
    return BoundaryOut.model_validate(boundary)


@router.get(
    "/{site_id}/boundary",
    response_model=BoundaryOut,
    summary="Получить границу площадки",
    description="Возвращает сохранённую границу площадки в формате GeoJSON.",
)
def get_boundary_endpoint(site_id: UUID, db: DBSession, _: AuthDep) -> BoundaryOut:
    get_site(db, site_id)
    boundary = get_boundary(db, site_id)
    return BoundaryOut.model_validate(boundary)
