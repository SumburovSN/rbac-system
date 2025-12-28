from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    users = relationship("UserRole", back_populates="role")
    rules = relationship("AccessRoleRule", back_populates="role")
