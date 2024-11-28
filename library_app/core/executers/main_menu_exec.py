from core.classes.app import AppExit
from core.classes.menu import MenuExit
from core.menu import main_menu, search_menu, book_manage_menu


@main_menu.mark(name="Управление книгами")
def book_manage_category() -> None:
    while True:
        try:
            book_manage_menu.show()
        except MenuExit:
            break

@main_menu.mark(name="Поиск")
def book_search_category() -> None:
    while True:
        try:
            search_menu.show()
        except MenuExit:
            break

@main_menu.mark(name="Выйти из приложения")
def exit_app_category() -> None:
    raise AppExit