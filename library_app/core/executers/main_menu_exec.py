from core.classes.app import AppExit, Library
from core.classes.menu import MenuExit
from core.menu import book_manage_menu, main_menu, search_menu


@main_menu.mark(name="Управление книгами")
def book_manage_category(app: Library) -> None:
    """
    Функция запустит меню 'Управление книгами'.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    book_manage_menu.set_app(app)
    while True:
        try:
            book_manage_menu.show()
        except MenuExit:
            break


@main_menu.mark(name="Поиск")
def book_search_category(app: Library) -> None:
    """
    Функция запустит меню 'Поиск'.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    search_menu.set_app(app)
    while True:
        try:
            search_menu.show()
        except MenuExit:
            break


@main_menu.mark(name="Выйти из приложения")
def exit_app_category() -> None:
    """
    Функция выхода из приложения.

    :return: None.
    """
    raise AppExit
