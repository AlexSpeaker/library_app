from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import Table
from core.menu import search_menu, selective_search_menu


@search_menu.mark(name="Найти книгу")
def find_book_category(app: Library) -> None:
    selective_search_menu.set_app(app)
    while True:
        try:
            selective_search_menu.show()
        except MenuExit:
            break


@search_menu.mark(name="Все книги")
def all_book_category(app: Library) -> None:
    books = app.orm.select(Book).all()
    table = Table(books, ("id", "title", "author", "year", "status"))
    table.show()


@search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
