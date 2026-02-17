from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class File_Data(Base):
    __tablename__= "File_Data"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    input_file_url= Column(String)
    output_file_url= Column(String)
    converted_from = Column(String)
    converted_to = Column(String)
    status = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime, default=datetime.utcnow)