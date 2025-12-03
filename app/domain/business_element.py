from dataclasses import dataclass


@dataclass
class BusinessElement:
    id: int | None
    code: str
    name: str

    @staticmethod
    def create(code: str, name: str):
        return BusinessElement(
            id=None,
            code=code,
            name=name
        )
