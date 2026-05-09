from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    login = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)  # bcrypt hash
    email = Column(String(128))

    # Связь с задачами
    tasks = relationship("Task", back_populates="owner", lazy="dynamic")