from sqlalchemy import Integer, String, Column
from core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password_hash = Column(String, nullable=False, unique=False)
