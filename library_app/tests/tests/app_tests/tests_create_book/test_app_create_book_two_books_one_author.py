from random import choices
from string import ascii_letters
from typing import Sequence

import pytest
from core.classes.app import Library
from core.db_models.author import Author
from core.db_models.book import Book
from tests.tests.utils import get_printed_text_and_input_text


@pytest.mark.app
def test_app_create_book_two_books_one_author(app_no_data: Library) -> None:
    """
    Создадим 2 книги в приложении, но укажем одного автора, ожидаем в БД: 2 книги и 1 автор.
    :param app_no_data: Приложение с пустой БД.
    :return: None.
    """

    # Убедимся, что в БД нет книг и авторов.
    books: Sequence[Book] = app_no_data.orm.select(Book).all()
    authors: Sequence[Author] = app_no_data.orm.select(Author).all()
    assert len(books) == 0
    assert len(authors) == 0

    book_1_title = "".join(choices(ascii_letters, k=10))
    book_2_title = "".join(choices(ascii_letters, k=10))
    author_first_name = "".join(choices(ascii_letters, k=10))
    author_last_name = "".join(choices(ascii_letters, k=10))

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами',
    # выбираем 'Добавить книгу', создаём 1-ю книгу,
    # выбираем 'Добавить книгу', создаём 2-ю книгу,
    # выходим из приложения.

    user_inputs = [
        "1",
        "1",
        book_1_title,
        f"{author_first_name} {author_last_name}",
        "1988",
        "1",
        book_2_title,
        f"{author_first_name} {author_last_name}",
        "1988",
        "5",
        "3",
    ]
    # Выполним сценарий, сами printed_text и input_text нас в этом тесте не интересуют.
    get_printed_text_and_input_text(app_no_data, user_inputs)

    # Убедимся, что книг две, а автор 1.
    new_books: Sequence[Book] = app_no_data.orm.select(Book).all()
    new_authors: Sequence[Author] = app_no_data.orm.select(Author).all()
    assert len(new_books) == 2
    assert len(new_authors) == 1
    assert set(book.title for book in new_books) == {book_1_title, book_2_title}
    assert new_authors[0].first_name == author_first_name
    assert new_authors[0].last_name == author_last_name
