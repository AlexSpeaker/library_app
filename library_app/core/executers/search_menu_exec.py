
from core.classes.menu import MenuExit
from core.menu import search_menu


@search_menu.mark(name="Найти книгу")
def find_book_category() -> None:
    pass

@search_menu.mark(name="Все книги")
def all_book_category() -> None:
    pass

@search_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit