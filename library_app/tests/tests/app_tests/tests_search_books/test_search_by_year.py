from typing import Sequence

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import check_books_print, get_printed_text_and_input_text


@pytest.mark.app
def test_search_by_year(app_with_data: Library) -> None:
    """
    Приложение ищет строгое соответствие.
    А так же мы точно знаем, что в БД есть 2 книги за 2019 год.
    Попробуем найти их.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """
    year = 2019

    # Убедимся, что в БД есть книги за 2019 год и их 2.
    books: Sequence[Book] = app_with_data.orm.select(Book).filter_soft(year=year)
    assert len(books) == 2

    # Сценарий: Запускаем приложение, заходим в 'Поиск',
    # выбираем 'Найти книгу',
    # выбираем 'Поиск по году издания',
    # выходим из приложения.
    user_inputs = ["2", "1", "3", str(year), "4", "3", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )

    # Проверяем, что все книги (вместе с данными) были показаны.
    check_books_print(books, app_with_data, printed_text)
    assert "Введите год издания книги (--exit для выхода)" in input_text
