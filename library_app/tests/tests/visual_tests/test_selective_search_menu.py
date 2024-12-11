import pytest
from core.classes.app import Library
from core.menu import selective_search_menu
from tests.tests.utils import check_menu


@pytest.mark.visual
def test_selective_search_menu(app_no_data: Library) -> None:
    """
    Тестируем визуальную часть. Выборочный поиск.

    :param app_no_data: Экземпляр класса Library.
    :return: None
    """
    # Сценарий: Запускаем приложение, заходим в 'Поиск', заходим в 'Найти книгу' и выходим из приложения.
    user_inputs = ["2", "1", "4", "3", "3"]
    check_menu(app_no_data, user_inputs, selective_search_menu)
