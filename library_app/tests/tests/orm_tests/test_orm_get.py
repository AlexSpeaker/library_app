from random import choice
from typing import Any, Dict, List, Optional

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_get(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим метод get.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Найдём все книги в БД.
    db = get_db_data(settings)
    bd_books: List[Dict[str, Any]] = db["books"]

    # Выберем случайную книгу.
    bd_book = choice(bd_books)

    # Найдём её через ORM
    orm_book: Optional[Book] = orm_with_data.select(Book).get(bd_book["id"])
    assert orm_book is not None
    assert orm_book.title == bd_book["title"]
    assert orm_book.id == bd_book["id"]
