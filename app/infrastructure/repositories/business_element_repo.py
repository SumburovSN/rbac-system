from sqlalchemy.orm import Session
from app.domain.repositories.business_element_repository import BusinessElementRepository
from app.domain.business_element import BusinessElement as DomainElement
from app.infrastructure.db.models.business_element import BusinessElement as DbElement


class BusinessElementRepositoryImpl(BusinessElementRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, element: DomainElement) -> DomainElement:
        db_el = DbElement(code=element.code, name=element.name)
        self.db.add(db_el)
        self.db.commit()
        self.db.refresh(db_el)
        return self._to_domain(db_el)

    def get_by_id(self, element_id: int) -> DomainElement | None:
        db_el = self.db.get(DbElement, element_id)
        return self._to_domain(db_el) if db_el else None

    def get_by_code(self, code: str) -> DomainElement | None:
        db_el = self.db.query(DbElement).filter(DbElement.code == code).first()
        return self._to_domain(db_el) if db_el else None

    def get_all(self) -> list[DomainElement]:
        db_list = self.db.query(DbElement).all()
        return [self._to_domain(e) for e in db_list]

    def update(self, element: DomainElement, data: dict) -> DomainElement:
        db_el = self.db.get(DbElement, element.id)
        if not db_el:
            raise ValueError("BusinessElement not found")
        for k, v in data.items():
            setattr(db_el, k, v)
        self.db.commit()
        self.db.refresh(db_el)
        return self._to_domain(db_el)

    @staticmethod
    def _to_domain(db: DbElement) -> DomainElement:
        return DomainElement(
            id=db.id,
            code=db.code,
            name=db.name
        )
