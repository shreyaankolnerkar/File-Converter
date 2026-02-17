from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.core import storage
from app.db.session import get_db
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_file_api(file: UploadFile, db: Session = Depends(get_db)):
    upload_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(upload_path, "wb") as f:
        f.write(await file.read())

    ext = file.filename.split(".")[-1]

    user_id, file_id = storage.create_file_record(
        db=db,
        filename=file.filename,
        converted_from=ext,
        converted_to="excel",
        status=0,
        expire_hours=24
    )

    return {
        "api_key": user_id,
        "file_id": file_id,
        "input_file_name": file.filename,
        "message": "Upload successful. Use this API key for authentication."
    }
