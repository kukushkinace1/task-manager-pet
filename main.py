from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.database import engine, Base, get_db
from core.deps import get_current_user
from core.security import get_password_hash, verify_password, create_access_token
from models.user import User
from models.task import Task
from schemas.auth import TokenResponse, LoginRequest
from schemas.user import UserRead, UserCreate
from routers.tasks import router as tasks_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo Manager")
app.include_router(tasks_router)


@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


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


@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid login or pass")

    token = create_access_token(user.id)

    return {"access_token": token}


@app.get("/health")
def health():
    return {"status": "ok"}
