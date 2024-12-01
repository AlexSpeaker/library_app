from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_delete_book_false(app_with_data: Library) -> None:
    """
    Начнём процесс удаления, но в конце передумаем. Книга должна остаться в базе.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Убедимся, что книга с id=1 существует.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Удалить книгу',
    # вводим id=1, отказываемся,
    # выходим из приложения.

    user_inputs = ["1", "2", "1", "n", "5", "3"]
    # Выполним сценарий, сами printed_text и input_text нас в этом тесте не интересуют.
    get_printed_text_and_input_text(app_with_data, user_inputs)

    book_exists: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book_exists is not None
