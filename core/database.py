from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL


# соединение с базой
engine = create_engine(DATABASE_URL)

# фабрика сессий, создает сессии. Сам комичу, сам отправляю
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#реестр
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
