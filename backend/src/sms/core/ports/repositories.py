from abc import ABC, abstractmethod

from src.sms.core.domain.models import Brand


class BrandRepository(ABC):
    @abstractmethod
    def create(self, brand: Brand) -> None:
        """Creates new brand"""
        raise NotImplementedError
