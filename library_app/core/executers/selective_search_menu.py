from typing import List, Sequence

from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.author import Author
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
    Ввод должен быть Имя Фамилия, или только Фамилия.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    author_name = get_not_empty_string(
        "Введите автора книги (ввод должен быть Имя Фамилия, или только Фамилия): "
    )
    name_obj = author_name.split(" ")
    first_name, last_name = name_obj if len(name_obj) == 2 else (None, name_obj[0])
    search_data = (
        dict(first_name=first_name, last_name=last_name)
        if first_name
        else dict(last_name=last_name)
    )
    authors: Sequence[Author] = app.orm.select(Author).filter_soft(**search_data)
    if not authors:
        print("Не найдено ни одного автора.")
        return
    books_list: List[Book] = []
    for author in authors:
        books = app.orm.select(Book).filter_strict(author_id=author.id)
        if books:
            books_list.extend(books)
    if not books_list:
        print(f"Не найдено ни одной книги автора '{author_name}'.")
        return
    data_list = get_data_books_for_table(books_list, app)
    table = Table(data_list, ("id", "title", "author", "year", "status"))
    table.show()


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
