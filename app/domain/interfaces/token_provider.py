from abc import ABC, abstractmethod

class TokenProvider(ABC):
    @abstractmethod
    def encode(self, data: dict) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> dict | None: ...

