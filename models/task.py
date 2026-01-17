from sqlalchemy import Integer, String, Column, Boolean, Text, ForeignKey
from core.database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, index=True, nullable=True)
    is_done = Column(Boolean, default=False, nullable=False)

    id_owner = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
