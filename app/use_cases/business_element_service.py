from typing import List
from app.domain.business_element import BusinessElement as DomainBusinessElement
from app.domain.repositories.business_element_repository import BusinessElementRepository
from app.api.schemas.rbac import BusinessElementCreate, BusinessElementUpdate


class BusinessElementService:
    def __init__(self, repo: BusinessElementRepository):
        self.repo = repo

    def create(self, data: BusinessElementCreate) -> DomainBusinessElement:
        # Проверка уникальности code
        existing_code = self.repo.get_by_code(data.code)
        if existing_code:
            raise ValueError("BusinessElement with this code already exists")
        domain_element = DomainBusinessElement.create(code=data.code, name=data.name)
        return self.repo.create(domain_element)

    def get_all(self) -> List[DomainBusinessElement]:
        return self.repo.get_all()

    def get(self, element_id: int) -> DomainBusinessElement:
        return self.repo.get_by_id(element_id)

    def update(self, element_id: int, data: BusinessElementUpdate) -> DomainBusinessElement:
        element = self.repo.get_by_id(element_id)
        if not element:
            raise ValueError("BusinessElement not found")

        update_data = data.model_dump(exclude_unset=True)

        if "code" in update_data:
            existing_code = self.repo.get_by_code(update_data["code"])
            if existing_code and existing_code.id != element_id:
                raise ValueError("BusinessElement with this code already exists")

        # if "name" in update_data:
        #     existing_name = self.repo.get_by_name(update_data["name"])
        #     if existing_name and existing_name.id != element_id:
        #         raise ValueError("BusinessElement with this name already exists")

        return self.repo.update(element, update_data)
