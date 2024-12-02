from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import Table, get_data_books_for_table
from core.menu import search_menu, selective_search_menu


@search_menu.mark(name="Найти книгу")
def find_book_category(app: Library) -> None:
    """
    Функция запустит меню 'Найти книгу'.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    selective_search_menu.set_app(app)
    while True:
        try:
            selective_search_menu.show()
        except MenuExit:
            break


@search_menu.mark(name="Все книги")
def all_book_category(app: Library) -> None:
    """
    Функция покажет все книги в библиотеке.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    books = app.orm.select(Book).all()
    if not books:
        print("Библиотека пуста.")
        return
    data_list = get_data_books_for_table(books, app)
    table = Table(data_list, ("id", "title", "author", "year", "status"))
    table.show()


@search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    """
    Функция выхода из меню.

    :return: None.
    """
    raise MenuExit
