from __future__ import annotations

from uuid import UUID

from pydantic import ConfigDict

from app.models.enums import UploadStatus, UploadType
from app.schemas.common import IdCreatedAt


class UploadOut(IdCreatedAt):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "created_at": "2025-01-01T00:00:00Z",
                    "site_id": "00000000-0000-0000-0000-000000000000",
                    "upload_type": "boundary",
                    "status": "uploaded",
                    "filename": "site.dxf",
                    "content_type": "application/octet-stream",
                    "storage_path": "storage/...",
                }
            ]
        }
    )
    site_id: UUID
    upload_type: UploadType
    status: UploadStatus
    filename: str
    content_type: str | None
    storage_path: str
