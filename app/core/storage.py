import os
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.models import File_Data

# folder where files are stored
UPLOAD_DIR = "uploads"


def upload_file_bytes(file_bytes: bytes, filename: str, content_type: str):
    """
    Save file bytes to local storage
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path


def create_file_record(
    db: Session,
    filename: str,
    converted_from: str,
    converted_to: str = "excel",
    expire_hours: int = 24,
    status: int = 0,
):
    user_id = str(uuid.uuid4())
    expired_at = datetime.utcnow() + timedelta(hours=expire_hours)

    file_record = File_Data(
        user_id=user_id,
        input_file_url=filename,
        output_file_url=None,
        converted_from=converted_from,
        converted_to=converted_to,
        status=status,
        created_at=datetime.utcnow(),
        expired_at=expired_at,
    )

    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return user_id, file_record.id
