from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base


class AccessRoleRule(Base):
    __tablename__ = "access_role_rules"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    element_id = Column(Integer, ForeignKey("business_elements.id"), nullable=False)

    read_permission = Column(Boolean, default=False)
    create_permission = Column(Boolean, default=False)
    update_permission = Column(Boolean, default=False)
    delete_permission = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint("role_id", "element_id", name="uq_role_element_rule"),
    )

    role = relationship("Role", back_populates="rules")
    element = relationship("BusinessElement", back_populates="rules")
