from uuid import UUID

from fastapi import APIRouter, File, UploadFile

from app.api.deps import AuthDep, DBSession
from app.models.enums import UploadType
from app.schemas.uploads import UploadOut
from app.services.sites import get_site
from app.services.uploads import delete_upload, list_uploads, save_upload

router = APIRouter()

upload_file = File(...)


@router.post(
    "/{site_id}/uploads/boundary",
    response_model=UploadOut,
    summary="Загрузить границы участка",
    description="Загружает файл границ участка (DWG/DXF) и сохраняет его в хранилище.",
)
def upload_boundary(
    site_id: UUID,
    db: DBSession,
    _: AuthDep,
    file: UploadFile = upload_file,
) -> UploadOut:
    get_site(db, site_id)
    upload = save_upload(db, site_id=site_id, upload_type=UploadType.boundary, file=file)
    return UploadOut.model_validate(upload)


@router.post(
    "/{site_id}/uploads/terrain",
    response_model=UploadOut,
    summary="Загрузить цифровую модель рельефа",
    description="Загружает файл рельефа (SHP/DEM/GeoTIFF) и сохраняет его в хранилище.",
)
def upload_terrain(
    site_id: UUID,
    db: DBSession,
    _: AuthDep,
    file: UploadFile = upload_file,
) -> UploadOut:
    get_site(db, site_id)
    upload = save_upload(db, site_id=site_id, upload_type=UploadType.terrain, file=file)
    return UploadOut.model_validate(upload)


@router.post(
    "/{site_id}/uploads/existing",
    response_model=UploadOut,
    summary="Загрузить существующие объекты",
    description="Загружает файл существующих объектов/коммуникаций (например, DWG) в хранилище.",
)
def upload_existing(
    site_id: UUID,
    db: DBSession,
    _: AuthDep,
    file: UploadFile = upload_file,
) -> UploadOut:
    get_site(db, site_id)
    upload = save_upload(db, site_id=site_id, upload_type=UploadType.existing, file=file)
    return UploadOut.model_validate(upload)


@router.get(
    "/{site_id}/uploads",
    response_model=list[UploadOut],
    summary="Список загруженных файлов",
    description="Возвращает список файлов, загруженных для площадки.",
)
def list_site_uploads(site_id: UUID, db: DBSession, _: AuthDep) -> list[UploadOut]:
    get_site(db, site_id)
    uploads = list_uploads(db, site_id=site_id)
    return [UploadOut.model_validate(u) for u in uploads]


@router.delete(
    "/{site_id}/uploads/{upload_id}",
    status_code=204,
    summary="Удалить загруженный файл",
    description="Удаляет файл из хранилища и запись о загрузке.",
)
def delete_site_upload(site_id: UUID, upload_id: UUID, db: DBSession, _: AuthDep) -> None:
    get_site(db, site_id)
    delete_upload(db, site_id=site_id, upload_id=upload_id)
