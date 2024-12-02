from typing import Tuple

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_delete_model(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим удаление модели.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что книга 'Незнайка на Луне' есть в БД.
    db = get_db_data(settings)
    assert len(db["authors"]) > 0
    titles = [data["title"] for data in db["books"]]
    assert "Незнайка на Луне" in titles

    # Пробуем найти книгу по названию.
    books: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Незнайка на Луне"
    )
    assert len(books) > 0
    book = books[0]

    # Удаляем книгу.
    orm_with_data.delete(book)

    # Убедимся, что книга 'Незнайка на Луне' удалена из БД.
    db = get_db_data(settings)
    titles = [data["title"] for data in db["books"]]
    assert "Незнайка на Луне" not in titles
