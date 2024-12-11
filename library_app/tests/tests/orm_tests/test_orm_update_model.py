from random import choices
from string import ascii_letters
from typing import Tuple

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_update_model(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим обновление модели.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Мы точно знаем, что книга 'Мастер и Маргарита' есть в БД.
    books: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Мастер и Маргарита"
    )
    assert len(books) > 0
    book = books[0]

    # Обновим модель.
    book.title = "".join(choices(ascii_letters, k=200))
    orm_with_data.update(book)

    # Убедимся, что книга 'Мастер и Маргарита' была обновлена.
    db = get_db_data(settings)

    # Найдём в бд книгу с новым названием.
    books_list = [data for data in db["books"] if data["title"] == book.title]

    # Книга найдена и id совпадают.
    assert len(books_list) == 1
    assert books_list[0]["id"] == book.id
