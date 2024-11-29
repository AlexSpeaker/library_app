from core.classes.app import Library
from core.classes.menu import MenuExit
from core.executers.utils import Table
from core.menu import search_menu


@search_menu.mark(name="Найти книгу")
def find_book_category(app: Library) -> None:
    pass


@search_menu.mark(name="Все книги")
def all_book_category(app: Library) -> None:
    books = app.orm.get_all_books()
    table = Table(books, ("id", "title", "author", "year", "status"))
    table.show()


@search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
