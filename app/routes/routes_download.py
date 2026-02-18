import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.auth import get_api_key
from app.core.storage import UPLOAD_DIR
from app.db.models import File_Data
from app.db.session import get_db

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/file/{file_id}")
def download_converted_file(
    file_id: int,
    user_id: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    file_record = db.query(File_Data).filter(File_Data.id == file_id, File_Data.user_id == user_id).first()

    if not file_record:
        raise HTTPException(404, "File not found for this API key")

    if not file_record.output_file_url:
        raise HTTPException(400, "File has not been converted yet")

    # ✅ Always resolve full path inside uploads
    file_path = os.path.join(UPLOAD_DIR, file_record.output_file_url)

    if not os.path.exists(file_path):
        raise HTTPException(
            404,
            f"Converted file {file_record.output_file_url} not found on server",
        )

    # ✅ Detect MIME type by extension
    ext = file_record.output_file_url.split(".")[-1].lower()

    if ext == "xlsx":
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif ext in ["jpg", "jpeg"]:
        media_type = "image/jpeg"
    elif ext == "png":
        media_type = "image/png"
    elif ext == "pdf":
        media_type = "application/pdf"
    else:
        media_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type=media_type,
    )
