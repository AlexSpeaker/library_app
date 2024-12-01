from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_give_book_true(app_with_data: Library) -> None:
    """
    Попробуем в приложении выдать книгу. Ожидаем, что книга поменяет свой статус.
    Бонусом проверим ошибки ввода.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Убедимся, что у книги с id=1 значение статуса будет True.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None
    assert book.status

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Выдать книгу читателю',
    # вводим пустое поле, вводим буквы, вводим id, которого не существует, вводим id=1,
    # выходим из приложения.
    user_inputs = ["1", "3", "", "ff", "5000", "3", "1", "5", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )
    # Убедимся, что у книги с id=1 значение статуса будет False.
    give_book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert give_book is not None
    assert not give_book.status

    # Проверим, что все надписи присутствуют.
    assert "Введите id книги (--exit для выхода)" in input_text
    assert "Поле не может быть пустым" in printed_text
    assert "ID должно быть числом" in printed_text
    assert "Ошибка! Книга с ID=5000 не существует" in printed_text
    assert f"Книга '{book.title}' была успешно выдана читателю" in printed_text

