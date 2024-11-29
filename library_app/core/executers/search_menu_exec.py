from core.classes.app import Library
from core.classes.menu import MenuExit
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
    pass
    # books = app.orm.get_all_books()
    # print_books(books)


@search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
