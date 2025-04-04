from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal
from pydantic import BaseModel

router = APIRouter()

class PasswordCreate(BaseModel):
    password: str


class PasswordResponse(BaseModel):
    service_name: str
    password: str


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


@router.post("/password/{service_name}", response_model=PasswordResponse)
def create_password(service_name: str, password: PasswordCreate, db: Session = Depends(get_db)):
    db_password = db.query(models.Password).filter(models.Password.service_name == service_name).first()
    if db_password: db_password.set_password(password.password)
    else:
        new_password = models.Password(service_name=service_name)
        new_password.set_password(password.password)
        db.add(new_password)
    db.commit()
    db.refresh(new_password if not db_password else db_password)
    return {"service_name": new_password.service_name if not db_password else db_password.service_name,
            "password": new_password.password_hash if not db_password else db_password.password_hash}


@router.get("/password/{service_name}", response_model=PasswordResponse)
def get_password(service_name: str, db: Session = Depends(get_db)):
    password_entry = db.query(models.Password).filter(models.Password.service_name == service_name).first()
    if password_entry:
        return {"service_name": password_entry.service_name, "password": password_entry.password_hash}
    raise HTTPException(status_code=404, detail="Password not found")


@router.get("/password/", response_model=list[PasswordResponse])
def search_password(service_name: str, db: Session = Depends(get_db)):
    passwords = db.query(models.Password).filter(models.Password.service_name.like(f'%{service_name}%')).all()
    return [{"service_name": p.service_name, "password": p.password_hash} for p in passwords]