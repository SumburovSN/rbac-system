from dataclasses import dataclass


@dataclass
class Role:
    id: int | None
    name: str
    description: str | None = None

    @staticmethod
    def create(name: str, description: str | None = None):
        return Role(id=None, name=name, description=description)
