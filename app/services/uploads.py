from __future__ import annotations

import os
import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import AppError
from app.models.enums import UploadType
from app.models.upload import Upload


def _ensure_storage_dir() -> Path:
    p = Path(settings.storage_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_upload(db: Session, *, site_id, upload_type: UploadType, file: UploadFile) -> Upload:
    storage_dir = _ensure_storage_dir()
    upload_id = uuid.uuid4()
    safe_name = os.path.basename(file.filename or "file")
    target = storage_dir / f"{upload_id}_{safe_name}"
    with target.open("wb") as out:
        out.write(file.file.read())

    upload = Upload(
        id=upload_id,
        site_id=site_id,
        upload_type=upload_type.value,
        filename=safe_name,
        content_type=file.content_type,
        storage_path=str(target),
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload


def list_uploads(db: Session, *, site_id) -> list[Upload]:
    return (
        db.query(Upload)
        .filter(Upload.site_id == site_id)
        .order_by(Upload.created_at.desc())
        .all()
    )


def get_upload(db: Session, *, site_id, upload_id) -> Upload:
    upload = db.query(Upload).filter(Upload.site_id == site_id, Upload.id == upload_id).first()
    if not upload:
        raise AppError("Файл не найден", status_code=404)
    return upload


def delete_upload(db: Session, *, site_id, upload_id) -> None:
    upload = get_upload(db, site_id=site_id, upload_id=upload_id)

    storage_dir = Path(settings.storage_dir).resolve()
    try:
        target = Path(upload.storage_path).resolve()
        if storage_dir in target.parents or target == storage_dir:
            if target.is_file():
                target.unlink(missing_ok=True)
    except OSError:
        pass

    db.delete(upload)
    db.commit()
