from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.business_element import BusinessElement

class BusinessElementRepository(ABC):

    @abstractmethod
    def create(self, element: BusinessElement) -> BusinessElement:
        pass

    @abstractmethod
    def get_by_id(self, element_id: int) -> BusinessElement | None:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> BusinessElement | None:
        pass

    @abstractmethod
    def get_all(self) -> List[BusinessElement]:
        pass

    @abstractmethod
    def update(self, element: BusinessElement, data: dict) -> BusinessElement:
        pass
