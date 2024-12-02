from typing import Any, Dict, List, Tuple

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_bulk_delete(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим массовое удаление.
    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что в БД есть книги:
    db = get_db_data(settings)
    bd_books_1: List[Dict[str, Any]] = db["books"]
    assert len(bd_books_1) > 0

    # Получим все книги и удалим их:
    orm_books: Tuple[Book, ...] = orm_with_data.select(Book).all()
    assert len(orm_books) == len(bd_books_1)
    orm_with_data.bulk_delete(*orm_books)

    # Убедимся, что в БД нет книг:
    db = get_db_data(settings)
    bd_books_2: List[Dict[str, Any]] = db["books"]
    assert len(bd_books_2) == 0
