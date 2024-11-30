from typing import Sequence

from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import (
    Table,
    get_data_books_for_table,
    get_not_empty_string,
    get_year,
)
from core.menu import selective_search_menu


@selective_search_menu.mark(name="Поиск по названию")
def search_by_title_category(app: Library) -> None:
    """
    Функция 'мягко' (достаточно набрать несколько букв)
    найдёт все совпадения по названию книги и покажет их пользователю.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    title = get_not_empty_string("Введите название книги: ")
    books: Sequence[Book] = app.orm.select(Book).filter_soft(title=title)
    if not books:
        print("Не найдено ни одного совпадения.")
        return
    data_list = get_data_books_for_table(books, app)
    table = Table(data_list, ("id", "title", "author", "year", "status"))
    table.show()


@selective_search_menu.mark(name="Поиск по автору")
def search_by_author_category(app: Library) -> None:
    """
    Функция 'мягко' (достаточно набрать несколько букв)
    найдёт все совпадения по автору книги и покажет их пользователю.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    # author = get_not_empty_string("Введите автора книги: ")
    # books: Sequence[Book] = app.orm.select(Book).filter_soft(author=author)
    # if not books:
    #     print("Не найдено ни одного совпадения.")
    #     return
    # table = Table(books, ("id", "title", "author", "year", "status"))
    # table.show()


@selective_search_menu.mark(name="Поиск по году издания")
def search_by_year_category(app: Library) -> None:
    """
    Функция 'строго' (нужно полное соответствие)
    найдёт все совпадения по году издания книги и покажет их пользователю.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    year = get_year("Введите год издания книги: ")
    books: Sequence[Book] = app.orm.select(Book).filter_strict(year=int(year))
    if not books:
        print("Не найдено ни одного совпадения.")
        return
    data_list = get_data_books_for_table(books, app)
    table = Table(data_list, ("id", "title", "author", "year", "status"))
    table.show()


@selective_search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    """
    Функция выхода из меню.

    :return: None.
    """
    raise MenuExit
