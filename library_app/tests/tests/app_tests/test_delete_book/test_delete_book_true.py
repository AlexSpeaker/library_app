from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_delete_book_true(app_with_data: Library) -> None:
    """
    Удалим книгу в приложении.
    Бонусом проверим ошибки ввода.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Убедимся, что книга с id=1 существует.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Удалить книгу',
    # вводим пустое поле, вводим буквы, вводим id, которого не существует, вводим id=1, подтверждаем,
    # выходим из приложения.

    user_inputs = ["1", "2", "", "ff", "5000", "2", "1", "y", "5", "3"]
    printed_text, input_text = get_printed_text_and_input_text(
        app_with_data, user_inputs
    )

    # Проверим, что книга удалена.
    assert app_with_data.orm.select(Book).get(pk=1) is None

    # Проверим, что все надписи присутствуют.
    assert "Поле не может быть пустым" in printed_text
    assert "ID должно быть числом" in printed_text
    assert "Ошибка! Книга с ID=5000 не существует" in printed_text
    assert f"Книга '{book.title}' была успешно удалена" in printed_text
    assert "Введите id книги" in input_text
    assert f"Вы действительно хотите удалить книгу '{book.title}' (N/y)" in input_text
