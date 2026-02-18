import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.converters.img_to_jpg import image_to_jpg
from app.core.auth import get_api_key
from app.core.storage import upload_file_bytes
from app.db.models import File_Data
from app.db.session import get_db

UPLOAD_DIR = "uploads"

router = APIRouter(prefix="/convert", tags=["convert"])


@router.post("/image-to-jpg/{file_id}")
def convert_image_to_jpg(
    file_id: int,
    user_id: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    file_record = db.query(File_Data).filter(File_Data.id == file_id, File_Data.user_id == user_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = os.path.join(UPLOAD_DIR, file_record.input_file_url)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Input file missing on server")

    with open(file_path, "rb") as f:
        image_bytes = f.read()

    jpg_bytes = image_to_jpg(image_bytes)

    output_url = file_record.input_file_url.rsplit(".", 1)[0] + ".jpg"

    upload_file_bytes(jpg_bytes, output_url, "image/jpeg")

    file_record.output_file_url = output_url
    file_record.status = 1
    db.commit()

    return {
        "file_id": file_id,
        "output_file_url": output_url,
        "message": "Image converted to JPG",
    }
