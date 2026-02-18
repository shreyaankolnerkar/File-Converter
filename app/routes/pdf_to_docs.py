import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.converters.pdf_to_docs import pdf_to_docx
from app.core.auth import get_api_key
from app.core.storage import UPLOAD_DIR, upload_file_bytes
from app.db.models import File_Data
from app.db.session import get_db

router = APIRouter(prefix="/convert", tags=["convert"])


@router.post("/pdf-to-docx/{file_id}")
def convert_pdf_to_docx(
    file_id: int,
    user_id: str = Depends(get_api_key),
    db: Session = Depends(get_db),
):
    file_record = db.query(File_Data).filter(File_Data.id == file_id, File_Data.user_id == user_id).first()
    if not file_record:
        raise HTTPException(404, "File not found")

    input_path = os.path.join(UPLOAD_DIR, file_record.input_file_url)

    if not os.path.exists(input_path):
        raise HTTPException(404, "Input file missing")

    with open(input_path, "rb") as f:
        pdf_bytes = f.read()

    docx_bytes = pdf_to_docx(pdf_bytes)

    output_url = file_record.input_file_url.rsplit(".", 1)[0] + ".docx"

    upload_file_bytes(
        docx_bytes,
        output_url,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    file_record.output_file_url = output_url
    file_record.converted_to = "docx"
    file_record.status = 1
    db.commit()

    return {
        "file_id": file_id,
        "output_file_url": output_url,
        "message": "PDF converted to DOCX",
    }
