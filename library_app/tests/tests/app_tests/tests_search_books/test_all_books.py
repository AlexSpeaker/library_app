from typing import Sequence

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import check_books_print, get_printed_text_and_input_text


@pytest.mark.app
def test_all_books(app_with_data: Library) -> None:
    """
    Попробуем в приложении получить список всех книг.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Убедимся, что база данных не пуста и содержит как минимум 3 книги.
    books: Sequence[Book] = app_with_data.orm.select(Book).all()
    assert len(books) >= 3

    # Сценарий: Запускаем приложение, заходим в 'Поиск',
    # выбираем 'Все книги',
    # выходим из приложения.
    user_inputs = ["2", "2", "3", "3"]
    printed_text, _ = get_printed_text_and_input_text(app_with_data, user_inputs)

    # Проверяем, что все книги (вместе с данными) были показаны.
    check_books_print(books, app_with_data, printed_text)
