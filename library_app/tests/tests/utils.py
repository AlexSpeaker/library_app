import json
import re
import threading
from typing import Any, Dict, List
from unittest.mock import patch

from core.classes.app import Library
from core.classes.menu import Menu
from settings.settings_class import Settings


def get_db_data(settings: Settings) -> Dict[str, Any]:
    """
    Функция читает БД из файла и возвращает её в виде словаря.

    :param settings: Настройки.
    :return:
    """
    db_path = settings.db_settings.db_base_path / settings.db_settings.name
    with open(db_path, "r", encoding="utf-8") as file:
        db: Dict[str, Any] = json.load(file)
    return db


def safe_to_execute_app(app: Library) -> None:
    """
    Безопасно запустит приложение, а если оно зависнет, то выдаст исключение.

    :param app: Экземпляр класса Library.
    :return: None.
    """

    timeout = 5.0
    thread = threading.Thread(target=app.run)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise AssertionError("Время выполнения превышено!")


def check_menu(app: Library, scenario: List[str], menu: Menu) -> None:
    """
    Функция тестирует наличие всех категорий в меню на экране пользователя.
    :param app: Экземпляр класса Library.
    :param scenario: Сценарий.
    :param menu: Экземпляр класса Menu.
    :return: None.
    """
    with patch("builtins.input", side_effect=scenario), patch(
        "builtins.print"
    ) as mock_print:
        safe_to_execute_app(app)
        printed_text = "".join(call.args[0] for call in mock_print.call_args_list)

    pattern = rf"\*\s+{menu.get_title()}" + r"((.+?)(?=\*{4,}))"
    menu_re = re.search(pattern, printed_text)
    assert menu_re is not None
    menu_str = menu_re.group(1)

    # Проверим, что все категории присутствуют в меню.
    for category in menu.get_menu_list():
        assert category in menu_str
