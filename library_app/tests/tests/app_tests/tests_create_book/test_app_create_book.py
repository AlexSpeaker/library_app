from datetime import datetime
from random import choices
from string import ascii_letters
from typing import Optional

import pytest
from core.classes.app import Library
from core.db_models.author import Author
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_app_create_book(app_no_data: Library) -> None:
    """
    Создадим книгу в приложении.
    Бонусом проверим ошибки ввода.

    :param app_no_data: Приложение с пустой БД.
    :return: None.
    """

    # Убедимся, что книги с ID=1 не существует.
    book: Optional[Book] = app_no_data.orm.select(Book).get(pk=1)
    assert book is None

    book_title = "".join(choices(ascii_letters, k=10))
    author_first_name = "".join(choices(ascii_letters, k=10))
    author_last_name = "".join(choices(ascii_letters, k=10))

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Добавить книгу',
    # вводим пустое название книги, вводим название книги,
    # вводим пустое поле автора, вводим автора,
    # вводим год пустым, символы, будущий год, валидный год,
    # выходим из приложения.

    user_inputs = [
        "1",
        "1",
        "",
        book_title,
        "",
        f"{author_first_name} {author_last_name}",
        "",
        "yyyy",
        f"{datetime.now().year + 1}",
        "1988",
        "5",
        "3",
    ]
    printed_text, input_text = get_printed_text_and_input_text(app_no_data, user_inputs)

    # Убедимся, что книга была создана:
    new_book: Optional[Book] = app_no_data.orm.select(Book).get(pk=1)
    assert new_book is not None
    assert new_book.title == book_title

    # Убедимся, что автор был создан:
    author: Optional[Author] = app_no_data.orm.select(Author).get(pk=1)
    assert author is not None
    assert author.first_name == author_first_name
    assert author.last_name == author_last_name

    # Проверим, что все надписи присутствуют.
    assert printed_text.count("Поле не может быть пустым") == 2
    assert printed_text.count("Год должен быть формата YYYY, где Y это цифра") == 2
    assert f"Год должен быть от 1000 до {datetime.now().year}" in printed_text

    assert "Введите название книги (--exit для выхода)" in input_text
    assert "Ведите автора (--exit для выхода)" in input_text
    assert "Введите год выпуска книги (--exit для выхода)" in input_text
