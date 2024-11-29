from core.classes.app import Library
from core.classes.menu import MenuExit
from core.executers.utils import get_not_empty_string, print_books
from core.menu import selective_search_menu


@selective_search_menu.mark(name="Поиск по названию")
def search_by_title_category(app: Library) -> None:
    title = get_not_empty_string("Введите название книги: ")
    books = app.orm.get_book_filter(title=title)
    print_books(books)


@selective_search_menu.mark(name="Поиск по автору")
def search_by_author_category(app: Library) -> None:
    author = get_not_empty_string("Введите автора книги: ")
    books = app.orm.get_book_filter(author=author)
    print_books(books)


@selective_search_menu.mark(name="Поиск по году издания")
def search_by_year_category(app: Library) -> None:
    year = get_not_empty_string("Введите год издания книги: ")
    books = app.orm.get_book_filter(year=year)
    print_books(books)


@selective_search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
