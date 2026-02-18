from fastapi import Depends, FastAPI
from sqlalchemy import text

from app.db.models import Base
from app.db.session import engine, get_db
from app.routes import (
    img_to_jpg_route,
    pdf_to_docs,
    routes_convert,
    routes_download,
    routes_upload,
)

app = FastAPI(title="File Converter")


@app.get("/db-test")
def db_test(db=Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "value": result}


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(routes_upload.router)
app.include_router(routes_convert.router)
app.include_router(img_to_jpg_route.router)
app.include_router(pdf_to_docs.router)
app.include_router(routes_download.router)
