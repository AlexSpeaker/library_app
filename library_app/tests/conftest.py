import json
from typing import Generator

import pytest
from core.classes.app import Library
from core.db_models.author import Author
from core.db_models.book import Book
from core.menu import main_menu
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.for_testing.settings import test_settings


@pytest.fixture
def settings() -> Settings:
    return test_settings


@pytest.fixture
def app(settings: Settings) -> Generator[Library, None, None]:
    yield Library(main_menu, settings)
    db_path = settings.db_settings.db_base_path / settings.db_settings.name
    with open(db_path, "w", encoding="utf-8") as file:
        json.dump({}, file, ensure_ascii=False, indent=2)


@pytest.fixture
def orm_with_data(settings: Settings) -> Generator[ORM, None, None]:
    orm = ORM(settings)
    author_1 = Author(first_name="Николай", last_name="Носов")
    author_2 = Author(first_name="Михаил", last_name="Булгаков")
    author_3 = Author(first_name="Сергей", last_name="Есенин")
    orm.bulk_create(author_1, author_2, author_3)
    book_1 = Book(title="Незнайка на Луне", author_id=author_1.id, year=2019)
    book_2 = Book(
        title="Приключения Незнайки и его друзей", author_id=author_1.id, year=2020
    )
    book_3 = Book(title="Незнайка в Солнечном городе", author_id=author_1.id, year=2019)
    book_4 = Book(title="Мастер и Маргарита", author_id=author_2.id, year=1967)
    book_5 = Book(title="Собачье сердце", author_id=author_2.id, year=1968)
    orm.bulk_create(book_1, book_2, book_3, book_4, book_5)
    yield orm
    db_path = settings.db_settings.db_base_path / settings.db_settings.name
    with open(db_path, "w", encoding="utf-8") as file:
        json.dump({}, file, ensure_ascii=False, indent=2)


@pytest.fixture
def orm_no_data(settings: Settings) -> Generator[ORM, None, None]:
    yield ORM(settings)
    db_path = settings.db_settings.db_base_path / settings.db_settings.name
    with open(db_path, "w", encoding="utf-8") as file:
        json.dump({}, file, ensure_ascii=False, indent=2)
