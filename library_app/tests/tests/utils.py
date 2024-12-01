import json
import re
import threading
from typing import Any, Dict, List, Optional, Sequence, Tuple
from unittest.mock import patch

from core.classes.app import Library
from core.classes.menu import Menu
from core.db_models.author import Author
from core.db_models.book import Book
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
    printed_text, _ = get_printed_text_and_input_text(app, scenario)

    pattern = rf"\*\s+{menu.get_title()}" + r"((.+?)(?=\*{4,}))"
    menu_re = re.search(pattern, printed_text)
    assert menu_re is not None
    menu_str = menu_re.group(1)

    # Проверим, что все категории присутствуют в меню.
    for category in menu.get_menu_list():
        assert category in menu_str


def get_printed_text_and_input_text(
    app: Library, scenario: List[str]
) -> Tuple[str, str]:
    """
    Функция выполнит сценарий и вернёт всё то, что выводилось на экран.
    :param app: Экземпляр класса Library.
    :param scenario: Сценарий.
    :return: Вернёт кортеж: 'print' текст, 'input' текст.
    """
    with patch("builtins.input", side_effect=scenario) as mock_input, patch(
        "builtins.print"
    ) as mock_print:
        safe_to_execute_app(app)
        printed_text = "".join(
            str(call.args[0]) if call.args else "" for call in mock_print.call_args_list
        )
        input_text = "".join(
            str(call.args[0]) if call.args else "" for call in mock_input.call_args_list
        )
    return printed_text, input_text


def check_books_print(books: Sequence[Book], app: Library, printed_text: str) -> None:
    """
    Проверит, что последовательность из книг была верно показана пользователю.

    :param books: Последовательность из книг.
    :param app: Экземпляр класса Library.
    :param printed_text: Текст, который был показан пользователю.
    :return:
    """
    for book in books:
        assert book.author_id
        author: Optional[Author] = app.orm.select(Author).get(pk=book.author_id)
        assert author is not None
        pattern = (
            rf"|\s*{book.id}\s*"
            rf"|\s*{book.title}\s*"
            rf"|\s*{''.join([author.first_name, author.last_name])}\s*"
            rf"|\s*{book.year}\s*"
            rf"|\s*{'В наличии' if book.status else 'Выдана'}\s*|"
        )
        assert re.search(pattern, printed_text)
