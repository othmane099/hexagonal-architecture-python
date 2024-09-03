from sqlalchemy.ext.asyncio import AsyncSession

from src.sms.core.domain.models import Brand
from src.sms.core.ports.repositories import BrandRepository


class BrandRepositoryImpl(BrandRepository):

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    def create(self, brand: Brand) -> None:
        self.session.add(brand)
