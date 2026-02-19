import json
import os

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.core import storage
from app.core.redis import redis_client
from app.db.session import get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_file_api(file: UploadFile, db: Session = Depends(get_db)):
    upload_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())

    ext = file.filename.split(".")[-1]

    CONVERSION_MAP = {
        "csv": "xlsx",
        "png": "jpg",
        "jpeg": "jpg",
        "webp": "jpg",
        "pdf": "docx",
    }

    target_ext = CONVERSION_MAP.get(ext)

    user_id, file_id = storage.create_file_record(
        db=db,
        filename=file.filename,
        converted_from=ext,
        converted_to=target_ext,
        status=0,
        expire_hours=24,
    )

    job_data = {
        "file_id": file_id,
        "filename": file.filename,
        "input_path": upload_path,
        "from_ext": ext,
        "to_ext": target_ext,
    }
    redis_client.rpush("file_conversion_queue", json.dumps(job_data))

    return {
        "api_key": user_id,
        "file_id": file_id,
        "input_file_name": file.filename,
        "message": "Upload successful. Use this API key for authentication.",
    }
