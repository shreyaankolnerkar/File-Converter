from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import File_Data
import uuid

def create_file_record(
    db: Session,
    filename: str,
    converted_from: str,
    converted_to: str = "excel",
    expire_hours: int = 24,
    status: int = 0
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
        expired_at=expired_at
    )

    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return user_id, file_record.id
