from typing import Tuple

import pytest
from core.db_models.book import Book
from core.orm.classes.orm import ORM


@pytest.mark.orm
def test_orm_filter_soft(orm_with_data: ORM) -> None:
    """
    Проверим мягкую фильтрацию.

    :param orm_with_data: ORM с данными в базе.
    :return: None.
    """

    # Мы точно знаем, что книги про Незнайку есть в БД, и их больше чем одна.
    # Найдём книгу по полному названию.
    books_1: Tuple[Book, ...] = orm_with_data.select(Book).filter_soft(
        title="Незнайка на Луне"
    )
    assert len(books_1) == 1
    book = books_1[0]
    assert book.title == "Незнайка на Луне"

    # Найдём книгу по частичному названию. Книг должно быть как минимум 2.
    books_2: Tuple[Book, ...] = orm_with_data.select(Book).filter_soft(title="Незнайка")
    assert len(books_2) >= 2
