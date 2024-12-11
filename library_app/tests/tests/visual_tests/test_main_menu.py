import pytest
from core.classes.app import Library
from core.menu import main_menu
from tests.tests.utils import check_menu


@pytest.mark.visual
def test_main_menu(app_no_data: Library) -> None:
    """
    Тестируем визуальную часть. Главное меню.

    :param app_no_data: Экземпляр класса Library.
    :return: None
    """

    # Сценарий: Запускаем приложение и выходим из приложения.
    user_inputs = ["3"]
    check_menu(app_no_data, user_inputs, main_menu)
