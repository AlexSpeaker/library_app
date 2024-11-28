from core.classes.app import Library
from core.classes.menu import MenuExit
from core.menu import book_manage_menu


@book_manage_menu.mark(name="Добавить книгу")
def add_book_category(app: Library) -> None:
    pass


@book_manage_menu.mark(name="Удалить книгу")
def delete_book_category(app: Library) -> None:
    pass


@book_manage_menu.mark(name="Выдать книгу читателю")
def give_book_category(app: Library) -> None:
    pass


@book_manage_menu.mark(name="<-- Назад")
def exit_category(app: Library) -> None:
    raise MenuExit
