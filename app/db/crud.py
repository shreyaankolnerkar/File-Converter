from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import File_Data
import uuid


def create_user_and_file(
    db: Session,
    input_file_url: str,
    converted_from: str,
    converted_to: str,
    status: int = 0,     
    expire_hours: int = 24
):

    user_id = str(uuid.uuid4())

    expired_at = datetime.utcnow() + timedelta(hours=expire_hours)

    file_record = File_Data(
        user_id=user_id,
        input_file_url=input_file_url,
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


def get_file_by_user(db: Session, user_id: str):
    return db.query(File_Data).filter(File_Data.user_id == user_id).all()


def get_file_by_id(db: Session, file_id: int):
    return db.query(File_Data).filter(File_Data.id == file_id).first()


def update_file_status(
    db: Session,
    file_id: int,
    status: int,
    output_file_url: str = None
):
    
    file_record = db.query(File_Data).filter(File_Data.id == file_id).first()
    if not file_record:
        return False

    file_record.status = status
    if output_file_url:
        file_record.output_file_url = output_file_url

    db.commit()
    db.refresh(file_record)
    return True


def authenticate_user(db: Session, user_id: str):
    user = db.query(File_Data).filter(File_Data.user_id == user_id).first()
    return bool(user)
