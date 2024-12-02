from typing import Any, Dict, List, Tuple

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_all(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим метод all.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Найдём все книги в БД.
    db = get_db_data(settings)
    bd_books: List[Dict[str, Any]] = db["books"]
    assert len(bd_books) > 0

    # Найдём все книги через ORM
    orm_books: Tuple[Book, ...] = orm_with_data.select(Book).all()

    # Проверим, что все книги найдены.
    assert len(orm_books) > 0
    assert len(orm_books) == len(bd_books)
    assert {book["id"] for book in bd_books} == {book.id for book in orm_books}
