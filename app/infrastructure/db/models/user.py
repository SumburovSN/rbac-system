from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # Связь с ролями
    roles = relationship("UserRole", back_populates="user")
