from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import get_not_empty_string, get_year
from core.menu import book_manage_menu


@book_manage_menu.mark(name="Добавить книгу")
def add_book_category(app: Library) -> None:
    """
    Пользователь вводит title, author и year,
    после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.

    :param app: Экземпляр класса Library.
    :return: None
    """
    title = get_not_empty_string("Введите название книги: ")
    author = get_not_empty_string("Ведите автора: ")
    year = get_year("Введите год выпуска книги: ")
    book = Book(title=title, author=author, year=year)
    app.orm.add_book(book)


@book_manage_menu.mark(name="Удалить книгу")
def delete_book_category(app: Library) -> None:
    pass


@book_manage_menu.mark(name="Выдать книгу читателю")
def give_book_category(app: Library) -> None:
    pass


@book_manage_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
