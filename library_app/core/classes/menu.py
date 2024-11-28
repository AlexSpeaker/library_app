from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

from core.classes.utils import print_menu

if TYPE_CHECKING:
    from core.classes.app import Library


class MenuExit(Exception):
    """Исключение, для выхода из меню."""


class NoCategory(Exception):
    """Исключение, если в меню не нашлось ни одной категории."""


class NoAppClass(Exception):
    """Исключение, если в меню не нашлось экземпляра класса Library."""


@dataclass
class CategoryInfo:
    """Класс содержит информацию об исполняющей функции категории и видимость этой категории."""

    func: Callable[["Library"], None]
    hidden: bool


class Menu:
    """Класс меню категорий"""

    __menu_dict: Dict[str, CategoryInfo] = {}
    __app: Optional["Library"] = None
    __message: str = "Сделайте Ваш выбор: "

    def __init__(self, *args: str, title: str) -> None:
        """
        Инициализация класса Menu.

        :param args: Перечень категорий меню. В этом же порядке они будут выводиться на экран.
        """
        self.__menu = list(args)
        self.__title = title

    def mark(self, name: str, hidden: bool = False) -> Callable[
        [Callable[["Library"], None]],
        Callable[["Library"], None],
    ]:
        """
        Декоратор регистрирующий функции, для категорий меню.

        :param name: Название категории меню.
        :param hidden: Скрытая ли это категория.
        :return: Ссылку на функцию декоратора.
        """

        def decorator(func: Callable[["Library"], None]) -> Callable[["Library"], None]:
            self.__menu_dict[name] = CategoryInfo(func, hidden)
            return func

        return decorator

    def set_message(self, message: str) -> None:
        """
        Задаёт сообщение, которое будет показано пользователю при выборе категории.
        По умолчанию - это 'Сделайте Ваш выбор: '.

        :param message: Сообщение (str).
        :return: None
        """
        self.__message = message

    def show(self) -> None:
        """
        Покажет меню и будет ждать ответа от пользователя.
        Если выбор валидный выполнит соответствующую функцию.

        :return: None
        """
        while True:
            self.__show_menu()
            choice_user = input(f"{self.__message}")
            result_validate, message = self.__validate_choice(choice_user)
            if not result_validate:
                print(message)
                continue
            break
        self.__execute(choice_user)

    def __execute(self, choice_user: str) -> None:
        """
        Функция выполнит привязанную к категории функцию.
        :param choice_user: Выбор пользователя.
        :return: None
        """
        if self.__app is None:
            raise NoAppClass(
                "В меню не нашлось экземпляра игры. Воспользуйтесь методом 'set_game'"
            )
        menu = self.__get_enabled_menu()
        func = self.__menu_dict[menu[int(choice_user) - 1]].func
        func(self.__app)

    def __get_enabled_menu(self) -> List[str]:
        """
        Вернёт список категорий меню, которые не спрятаны.

        :return: Список категорий List[str].
        """
        if not self.__menu_dict:
            raise NoCategory(
                f"В меню '{self.__title}' нет зарегистрированных функций для категорий."
            )
        return [
            menu
            for menu in self.__menu
            if self.__menu_dict.get(menu) and not self.__menu_dict[menu].hidden
        ]

    def __show_menu(self) -> None:
        """
        Покажет красивое меню.

        :return: None
        """
        menu = self.__get_enabled_menu()
        print_menu(menu, self.__title)

    def __validate_choice(self, user_choice: str) -> Tuple[bool, str]:
        """
        Проверит правильно ли ввёл категорию пользователь при выборе категории.

        :param user_choice: Выбор пользователя (str)
        :return: (True, 'OK') если всё хорошо, иначе (True, 'Информация пользователю, что он не так делает').
        """
        try:
            choice_int = int(user_choice)
        except ValueError:
            return False, "Вводить нужно только цифры!"
        if choice_int < 1 or choice_int > len(self.__get_enabled_menu()):
            return False, "Вне диапазона меню!"
        return True, "OK"

    def set_app(self, app: "Library") -> None:
        """
        Передаёт меню экземпляр класса Library.

        :param app: Экземпляр класса Library.
        :return: None
        """
        self.__app = app
