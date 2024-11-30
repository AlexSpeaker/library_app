import pytest
from core.classes.app import Library
from core.menu import book_manage_menu, main_menu, search_menu, selective_search_menu
from tests.tests.utils import check_menu


@pytest.mark.visual
def test_main_menu(app: Library) -> None:
    """
    Тестируем визуальную часть. Главное меню.

    :param app: Экземпляр класса Library.
    :return: None
    """

    # Сценарий: Запускаем приложение и выходим из приложения.
    user_inputs = ["3"]
    check_menu(app, user_inputs, main_menu)


@pytest.mark.visual
def test_book_manage_menu(app: Library) -> None:
    """
    Тестируем визуальную часть. Управление книгами.

    :param app: Экземпляр класса Library.
    :return: None
    """

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами' и выходим из приложения.
    user_inputs = ["1", "5", "3"]
    check_menu(app, user_inputs, book_manage_menu)


@pytest.mark.visual
def test_search_menu(app: Library) -> None:
    """
    Тестируем визуальную часть. Меню поиска.

    :param app: Экземпляр класса Library.
    :return: None
    """
    # Сценарий: Запускаем приложение, заходим в 'Поиск' и выходим из приложения.
    user_inputs = ["2", "3", "3"]
    check_menu(app, user_inputs, search_menu)

@pytest.mark.visual
def test_selective_search_menu(app: Library) -> None:
    """
    Тестируем визуальную часть. Выборочный поиск.

    :param app: Экземпляр класса Library.
    :return: None
    """
    # Сценарий: Запускаем приложение, заходим в 'Поиск', заходим в 'Найти книгу' и выходим из приложения.
    user_inputs = ["2", "1", "4", "3", "3"]
    check_menu(app, user_inputs, selective_search_menu)