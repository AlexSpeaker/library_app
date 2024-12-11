from typing import Sequence

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import check_books_print, get_printed_text_and_input_text


@pytest.mark.app
def test_search_by_title(app_with_data: Library) -> None:
    """
    Приложение ищет не строгое соответствие.
    А так же мы точно знаем, что в БД есть книги про Незнайку и их 3 шт.
    Попробуем найти их.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    book_name = "незн"

    # Убедимся, что в БД есть книги про Незнайку и их 3 шт.
    books: Sequence[Book] = app_with_data.orm.select(Book).filter_soft(title=book_name)
    assert len(books) == 3

    # Сценарий: Запускаем приложение, заходим в 'Поиск',
    # выбираем 'Найти книгу',
    # выбираем 'Поиск по названию',
    # выходим из приложения.
    user_inputs = ["2", "1", "1", book_name, "4", "3", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )

    # Проверяем, что все книги (вместе с данными) были показаны.
    check_books_print(books, app_with_data, printed_text)
    assert "Введите название книги (--exit для выхода)" in input_text
