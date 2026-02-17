from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.auth import get_api_key
from app.db.session import get_db
from app.db.models import File_Data
import os

router = APIRouter(prefix="/download", tags=["download"])

@router.get("/file/{file_id}")
def download_converted_file(
    file_id: int,
    user_id: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    
    file_record = db.query(File_Data).filter(File_Data.id == file_id, File_Data.user_id == user_id).first()
    if not file_record:
        raise HTTPException(404, "File not found for this API key")

    if not file_record.output_file_url:
        raise HTTPException(400, "File has not been converted yet")

    output_path = file_record.output_file_url
    if not os.path.exists(output_path):
        raise HTTPException(404, f"Converted file {output_path} not found on server")

    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
