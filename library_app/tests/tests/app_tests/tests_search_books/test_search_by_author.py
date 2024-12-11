from typing import Sequence

import pytest
from core.classes.app import Library
from core.db_models.author import Author
from core.db_models.book import Book
from tests.tests.utils import check_books_print, get_printed_text_and_input_text


@pytest.mark.app
def test_search_by_author(app_with_data: Library) -> None:
    """
    Приложение ищет не строгое соответствие.
    А так же мы точно знаем, что в БД есть книги Николая Носова и их 3 шт.
    Попробуем найти их.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """
    author_name = "ник нос"

    # Убедимся, что в БД есть книги Николая Носова и их 3 шт.
    authors: Sequence[Author] = app_with_data.orm.select(Author).filter_strict(
        first_name="Николай", last_name="Носов"
    )
    assert len(authors) == 1
    author: Author = authors[0]
    books: Sequence[Book] = app_with_data.orm.select(Book).filter_strict(
        author_id=author.id
    )
    assert len(books) == 3

    # Сценарий: Запускаем приложение, заходим в 'Поиск',
    # выбираем 'Найти книгу',
    # выбираем 'Поиск по автору',
    # выходим из приложения.
    user_inputs = ["2", "1", "2", author_name, "4", "3", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )

    # Проверяем, что все книги (вместе с данными) были показаны.
    check_books_print(books, app_with_data, printed_text)
    assert (
        "Введите автора книги (ввод должен быть Имя Фамилия, или только Фамилия) (--exit для выхода)"
        in input_text
    )
