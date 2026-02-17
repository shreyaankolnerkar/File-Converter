from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.db.session import get_db, engine
from app.db.models import Base
from app.routes import routes_upload
from app.routes import routes_convert
from app.routes import routes_download

app = FastAPI(title = "File Converter")

@app.get("/db-test")
def db_test(db=Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "value": result}

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(routes_upload.router)
app.include_router(routes_convert.router)
app.include_router(routes_download.router)