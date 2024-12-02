import pytest
from core.classes.app import Library
from core.menu import search_menu
from tests.tests.utils import check_menu


@pytest.mark.visual
def test_search_menu(app_no_data: Library) -> None:
    """
    Тестируем визуальную часть. Меню поиска.

    :param app_no_data: Экземпляр класса Library.
    :return: None
    """
    # Сценарий: Запускаем приложение, заходим в 'Поиск' и выходим из приложения.
    user_inputs = ["2", "3", "3"]
    check_menu(app_no_data, user_inputs, search_menu)
