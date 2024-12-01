from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_accept_book_false(app_with_data: Library) -> None:
    """
    Попробуем принять книгу, которую уже приняли ранее.
    Ожидаем сообщение, что книга уже была принята ранее,
    а так же ожидаем, что статус у книги не поменялся.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Убедимся, что у книги с id=1 значение статуса будет True.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None
    assert book.status

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Принять книгу',
    # вводим id=1,
    # выходим из приложения.
    user_inputs = ["1", "4", "1", "5", "3"]
    printed_text, _ = get_printed_text_and_input_text(app_with_data, user_inputs)

    # Убедимся, что статус книги не изменился.
    accept_book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert accept_book is not None
    assert accept_book.status

    assert (
        f"Ошибка! Книга '{book.title}' ранее уже была возвращена в библиотеку"
        in printed_text
    )
