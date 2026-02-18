import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.converters.csv_to_excel import csv_to_excel
from app.core.auth import get_api_key
from app.db.models import File_Data
from app.db.session import get_db

router = APIRouter(prefix="/convert", tags=["convert"])

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/csv-to-excel/{file_id}")
def convert_csv_to_excel(file_id: int, user_id: str = Depends(get_api_key), db: Session = Depends(get_db)):
    file_record = db.query(File_Data).filter(File_Data.id == file_id, File_Data.user_id == user_id).first()
    if not file_record:
        raise HTTPException(404, "File not found for this API key")

    if not file_record.input_file_url.endswith(".csv"):
        raise HTTPException(400, "Only CSV files can be converted to Excel")

    input_path = os.path.join("uploads", file_record.input_file_url)
    if not os.path.exists(input_path):
        raise HTTPException(404, f"Input file {input_path} not found")

    with open(input_path, "rb") as f:
        csv_bytes = f.read()

    excel_bytes = csv_to_excel(csv_bytes)

    excel_filename = f"{os.path.splitext(file_record.input_file_url)[0]}.xlsx"
    output_path = os.path.join(OUTPUT_DIR, excel_filename)
    with open(output_path, "wb") as f:
        f.write(excel_bytes)

    file_record.output_file_url = output_path
    file_record.status = 1
    db.commit()
    db.refresh(file_record)

    return {"message": "Conversion successful", "output_file_url": output_path}
