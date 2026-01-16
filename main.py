from fastapi import FastAPI, Depends, HTTPException

from core.database import engine, Base, get_db
from core.security import get_password_hash

from models.user import User
from schemas.user import UserRead, UserCreate

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


Base.metadata.create_all(bind=engine)
app = FastAPI(title="ToDo Manager")


@app.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):

    is_old_user = db.query(User).filter(User.email == user.email).first()
    if is_old_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    hash_pass = get_password_hash(user.password)

    new_user = User(email=user.email, password_hash=hash_pass)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered")

    return new_user


@app.get("/health")
def health():
    return {"status": "ok"}
