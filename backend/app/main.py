from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import get_db

app = FastAPI(title="Scrum App")

@app.get("/")
def inicio():
    return {"mensaje": "Scrum App funcionando"}

@app.get("/db-test")
def probar_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"base_de_datos": "conectada"}