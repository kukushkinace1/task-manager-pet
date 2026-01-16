from fastapi import FastAPI, Depends, HTTPException
from core.database import engine, Base, get_db
from core.security import get_password_hash
from models.user import User
from sqlalchemy.orm import Session
from schemas.user import UserRead, UserCreate, BaseModel, EmailStr

Base.metadata.create_all(bind=engine)
app = FastAPI(title="ToDo Manager")


@app.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):

    is_old_user = db.query(User).filter(User.email == user.email).first()
    if is_old_user:
        raise HTTPException(status_code=400, detail="Email is already redistered")

    hash_pass = get_password_hash(user.password)

    new_user = User(email=user.email, password_hash=hash_pass)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/health")
def health():
    return {"status": "ok"}
