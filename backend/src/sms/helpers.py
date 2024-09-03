from src.sms.core.domain.models import Brand
from src.sms.core.exceptions import EntityNotFound


async def get_existed_entity_by_id(uow, brand_id: int) -> Brand:
    """Uses find_by_id method which should be already existed in repository of uow passed as argument."""
    brand = await uow.repository.find_by_id(brand_id)
    if not brand:
        raise EntityNotFound("Brand not found with given id")
    return brand
