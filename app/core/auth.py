from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.models import File_Data
from app.db.session import get_db


def get_api_key(user_id: str = Header(..., alias="X-API-Key"), db: Session = Depends(get_db)):
    user = db.query(File_Data).filter(File_Data.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user_id
