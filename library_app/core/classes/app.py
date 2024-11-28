from typing import TYPE_CHECKING


class AppExit(Exception):
    """Исключение, для выхода из программы."""


if TYPE_CHECKING:
    from core.classes.menu import Menu


class Library:
    """Класс приложения."""

    def __init__(self, start_menu: "Menu") -> None:
        """Инициализация класса."""
        self.__start_menu = start_menu
        self.__start_menu.set_app(self)

    def run(self) -> None:
        """
        Запуск главного меню.

        :return: None.
        """
        while True:
            try:
                self.__start_menu.show()
            except AppExit:
                exit(0)
