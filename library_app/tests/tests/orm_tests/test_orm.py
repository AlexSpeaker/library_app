from random import choice, choices
from string import ascii_letters
from typing import Any, Dict, List, Optional, Tuple

import pytest
from core.db_models.author import Author
from core.db_models.book import Book
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_add_model(orm_no_data: ORM, settings: Settings) -> None:
    """
    Проверим создание модели.

    :param orm_no_data: ORM с пустой базой.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что база данных пустая.
    db = get_db_data(settings)
    assert len(db) == 0

    # Создадим модель и проверим её в БД.
    author_1 = Author(first_name="Николай", last_name="Носов")
    orm_no_data.add(author_1)
    assert author_1.id is not None

    # Убедимся, что запись есть в БД.
    db = get_db_data(settings)
    assert len(db["authors"]) > 0
    assert db["authors"][0]["id"] == author_1.id
    assert db["authors"][0]["first_name"] == author_1.first_name
    assert db["authors"][0]["last_name"] == author_1.last_name


@pytest.mark.orm
def test_orm_delete_model(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим удаление модели.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что книга 'Незнайка на Луне' есть в БД.
    db = get_db_data(settings)
    assert len(db["authors"]) > 0
    titles = [data["title"] for data in db["books"]]
    assert "Незнайка на Луне" in titles

    # Пробуем найти книгу по названию.
    books: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Незнайка на Луне"
    )
    assert len(books) > 0
    book = books[0]

    # Удаляем книгу.
    orm_with_data.delete(book)

    # Убедимся, что книга 'Незнайка на Луне' удалена из БД.
    db = get_db_data(settings)
    titles = [data["title"] for data in db["books"]]
    assert "Незнайка на Луне" not in titles


@pytest.mark.orm
def test_orm_update_model(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим обновление модели.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Мы точно знаем, что книга 'Мастер и Маргарита' есть в БД.
    books: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Мастер и Маргарита"
    )
    assert len(books) > 0
    book = books[0]

    # Обновим модель.
    book.title = "".join(choices(ascii_letters, k=200))
    orm_with_data.update(book)

    # Убедимся, что книга 'Мастер и Маргарита' была обновлена.
    db = get_db_data(settings)

    # Найдём в бд книгу с новым названием.
    books_list = [data for data in db["books"] if data["title"] == book.title]

    # Книга найдена и id совпадают.
    assert len(books_list) == 1
    assert books_list[0]["id"] == book.id


@pytest.mark.orm
def test_orm_filter_strict(orm_with_data: ORM) -> None:
    """
    Проверим строгую фильтрацию.

    :param orm_with_data: ORM с данными в базе.
    :return: None.
    """

    # Найдём книгу по полному названию.
    books_1: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Незнайка на Луне"
    )
    assert len(books_1) == 1
    book = books_1[0]
    assert book.title == "Незнайка на Луне"

    # Найдём книгу по частичному названию. Книг не должно найти.
    books_2: Tuple[Book, ...] = orm_with_data.select(Book).filter_strict(
        title="Незнайка"
    )
    assert len(books_2) == 0


@pytest.mark.orm
def test_orm_filter_soft(orm_with_data: ORM) -> None:
    """
    Проверим мягкую фильтрацию.

    :param orm_with_data: ORM с данными в базе.
    :return: None.
    """

    # Мы точно знаем, что книги про Незнайку есть в БД, и их больше чем одна.
    # Найдём книгу по полному названию.
    books_1: Tuple[Book, ...] = orm_with_data.select(Book).filter_soft(
        title="Незнайка на Луне"
    )
    assert len(books_1) == 1
    book = books_1[0]
    assert book.title == "Незнайка на Луне"

    # Найдём книгу по частичному названию. Книг должно быть как минимум 2.
    books_2: Tuple[Book, ...] = orm_with_data.select(Book).filter_soft(title="Незнайка")
    assert len(books_2) >= 2


@pytest.mark.orm
def test_orm_all(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим метод all.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Найдём все книги в БД.
    db = get_db_data(settings)
    bd_books: List[Dict[str, Any]] = db["books"]
    assert len(bd_books) > 0

    # Найдём все книги через ORM
    orm_books: Tuple[Book, ...] = orm_with_data.select(Book).all()

    # Проверим, что все книги найдены.
    assert len(orm_books) > 0
    assert len(orm_books) == len(bd_books)
    assert {book["id"] for book in bd_books} == {book.id for book in orm_books}


@pytest.mark.orm
def test_orm_get(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим метод get.

    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Найдём все книги в БД.
    db = get_db_data(settings)
    bd_books: List[Dict[str, Any]] = db["books"]

    # Выберем случайную книгу.
    bd_book = choice(bd_books)

    # Найдём её через ORM
    orm_book: Optional[Book] = orm_with_data.select(Book).get(bd_book["id"])
    assert orm_book is not None
    assert orm_book.title == bd_book["title"]
    assert orm_book.id == bd_book["id"]


@pytest.mark.orm
def test_orm_bulk_delete(orm_with_data: ORM, settings: Settings) -> None:
    """
    Проверим массовое удаление.
    :param orm_with_data: ORM с данными в базе.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что в БД есть книги:
    db = get_db_data(settings)
    bd_books_1: List[Dict[str, Any]] = db["books"]
    assert len(bd_books_1) > 0

    # Получим все книги и удалим их:
    orm_books: Tuple[Book, ...] = orm_with_data.select(Book).all()
    assert len(orm_books) == len(bd_books_1)
    orm_with_data.bulk_delete(*orm_books)

    # Убедимся, что в БД нет книг:
    db = get_db_data(settings)
    bd_books_2: List[Dict[str, Any]] = db["books"]
    assert len(bd_books_2) == 0


@pytest.mark.orm
def test_orm_bulk_create(orm_no_data: ORM, settings: Settings) -> None:
    """
    Проверим массовое создание моделей.
    :param orm_no_data: ORM с пустой базой.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что база данных пустая.
    db = get_db_data(settings)
    assert len(db) == 0

    # Создадим модели и сохраним их через метод bulk_create.
    author_1 = Author(first_name="Николай", last_name="Носов")
    author_2 = Author(first_name="Михаил", last_name="Булгаков")
    author_3 = Author(first_name="Сергей", last_name="Есенин")
    orm_no_data.bulk_create(author_1, author_2, author_3)

    # Проверим записи в БД.
    db = get_db_data(settings)
    assert len(db) > 0
    assert {author_1.last_name, author_2.last_name, author_3.last_name} == {
        data["last_name"] for data in db["authors"]
    }
