import pytest
from sqlalchemy import asc, desc

from src.sms.core.domain.models import Brand
from src.sms.helpers import get_column, order_by_column


def test_get_column_valid():
    column = get_column(Brand, "name")
    assert column == Brand.name


def test_get_column_invalid():
    column = get_column(Brand, "non_existent_column")
    assert column is None


@pytest.mark.parametrize(
    "direction, expected",
    [
        ("asc", asc(Brand.name)),
        ("desc", desc(Brand.name)),
        ("ASC", asc(Brand.name)),
        ("DESC", desc(Brand.name)),
    ],
)
def test_order_by_column_valid(direction, expected):
    column = Brand.name
    result = order_by_column(column, direction)
    assert str(result) == str(expected)


def test_order_by_column_invalid_column():
    result = order_by_column(None, "asc")
    assert result is None


def test_order_by_column_invalid_direction():
    column = Brand.name
    result = order_by_column(column, "invalid_direction")
    assert str(result) == str(asc(column))
