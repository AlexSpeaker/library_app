import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from core.db_models.book import Book
from core.orm.utils import get_next_id
from settings.settings_class import Settings


class ORMException(Exception):
    """Исключения в ORM"""


class BaseORM:
    def __init__(self, settings: Settings):
        self.__settings: Settings = settings
        db_dir: Path = settings.db_settings.db_base_path
        db_name: str = settings.db_settings.name
        self.__db_path: Path = db_dir / db_name

    def _get_database(self) -> Dict[str, Dict[str, Any]]:
        with open(self.__db_path, "r", encoding="utf-8") as file:
            db = json.load(file)
        if not isinstance(db, dict):
            raise ValueError("Загруженные данные не являются словарем.")
        return db

    def _save_db(self, db: Dict[str, Dict[str, Any]]) -> None:
        with open(self.__db_path, "w", encoding="utf-8") as file:
            json.dump(
                db, file, ensure_ascii=False, indent=4
            )  # Почему-то у меня тут pycharm ругается, хотя у mypy вопросов нет.


class BookORMSafeMethods(BaseORM):
    def get_all_books(self) -> Tuple[Book, ...]:
        db = self._get_database()
        return tuple(Book(id=key, **value) for key, value in db.items())

    def get_book_filter(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[str] = None,
    ) -> Tuple[Book, ...]:
        books = self.get_all_books()
        return tuple(
            filter(
                lambda book: book.looks_like(title=title, author=author, year=year),
                books,
            )
        )

    def get_book(self, book_id: int | str) -> Book:
        book_id = str(book_id)
        db = self._get_database()
        pre_book = db.get(book_id)
        if not pre_book:
            raise ORMException
        return Book(id=book_id, **pre_book)


class ORM(BookORMSafeMethods):
    def __init__(self, settings: Settings):
        super().__init__(settings)

    def delete_book(self, book: Book) -> None:
        book_bd = self.get_book(book.id)
        db = self._get_database()
        db.pop(book_bd.id)
        self._save_db(db)

    def add_book(self, book: Book) -> None:
        db = self._get_database()
        new_id = str(get_next_id(db))
        data = book.to_dict()
        data.pop("id")
        db[new_id] = data
        self._save_db(db)

    def update_book(self, book: Book) -> None:
        book_bd = self.get_book(book.id)
        db = self._get_database()
        data = book.to_dict()
        data.pop("id")
        db[book_bd.id].update(data)
        self._save_db(db)
