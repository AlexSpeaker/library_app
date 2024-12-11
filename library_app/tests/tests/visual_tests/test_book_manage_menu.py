import pytest
from core.classes.app import Library
from core.menu import book_manage_menu
from tests.tests.utils import check_menu


@pytest.mark.visual
def test_book_manage_menu(app_no_data: Library) -> None:
    """
    Тестируем визуальную часть. Управление книгами.

    :param app_no_data: Экземпляр класса Library.
    :return: None
    """

    # Сценарий: Запускаем приложение, заходим в 'Управление книгами' и выходим из приложения.
    user_inputs = ["1", "5", "3"]
    check_menu(app_no_data, user_inputs, book_manage_menu)
