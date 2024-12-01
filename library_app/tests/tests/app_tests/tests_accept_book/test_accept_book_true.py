from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_accept_book_true(app_with_data: Library) -> None:
    """
    Попробуем в приложении принять книгу. Ожидаем, что книга поменяет свой статус.
    Бонусом проверим ошибки ввода.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Выдадим книгу через ORM.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None
    book.status = False
    app_with_data.orm.update(book)

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Принять книгу',
    # вводим пустое поле, вводим буквы, вводим id, которого не существует, вводим id=1,
    # выходим из приложения.
    user_inputs = ["1", "4", "", "ff", "5000", "4", "1", "5", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )
    # Убедимся, что у книги с id=1 значение статуса будет True.
    accept_book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert accept_book is not None
    assert accept_book.status

    # Проверим, что все надписи присутствуют.
    assert "Введите id книги (--exit для выхода)" in input_text
    assert "Поле не может быть пустым" in printed_text
    assert "ID должно быть числом" in printed_text
    assert "Ошибка! Книга с ID=5000 не существует" in printed_text
    assert f"Книга '{book.title}' была успешно возвращена в библиотеку" in printed_text

