from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_give_book_false(app_with_data: Library) -> None:
    """
    Попробуем выдать книгу, которую уже выдали ранее.
    Ожидаем сообщение, что книга уже была выдана,
    а так же ожидаем, что статус у книги не поменялся.

    :param app_with_data: Приложение с данными в базе.
    :return: None.
    """

    # Выдадим книгу через ORM.
    book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert book is not None
    book.status = False
    app_with_data.orm.update(book)

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Выдать книгу читателю',
    # вводим id=1,
    # выходим из приложения.
    user_inputs = ["1", "3", "1", "5", "3"]
    printed_text, _ = get_printed_text_and_input_text(app_with_data, user_inputs)

    # Убедимся, что статус книги не изменился.
    give_book: Optional[Book] = app_with_data.orm.select(Book).get(pk=1)
    assert give_book is not None
    assert not give_book.status

    assert (
        f"Ошибка! Книга '{give_book.title}' ранее уже была выдана читателю"
        in printed_text
    )
