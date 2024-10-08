import enum

from sqlalchemy import asc, desc

from src.sms.core.domain.models import Brand, Category
from src.sms.core.exceptions import EntityNotFound


async def get_existed_entity_by_id(uow, entity_id: int) -> Brand | Category:
    """Uses find_by_id method which should be already existed in repository of uow passed as argument."""
    entity = await uow.repository.find_by_id(entity_id)
    if not entity:
        raise EntityNotFound("Brand not found with given id")
    return entity


def get_column(model, column_name: str):
    """Retrieves a column from the model by its name"""
    return getattr(model, column_name, None)


class SortDirection(str, enum.Enum):
    ASC = "asc"
    DESC = "desc"


def order_by_column(column, direction: SortDirection):
    """Applies sorting direction (asc/desc) to a given column"""
    if column is not None:
        if direction.lower() == "desc":
            return desc(column)
        else:
            return asc(column)
    return None
