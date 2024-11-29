from typing import TYPE_CHECKING

from core.orm.classes import ORM
from settings.settings_class import Settings


class AppExit(Exception):
    """Исключение, для выхода из программы."""


if TYPE_CHECKING:
    from core.classes.menu import Menu


class Library:
    """Класс приложения."""

    def __init__(self, start_menu: "Menu", settings: Settings) -> None:
        """Инициализация класса."""
        self.__start_menu = start_menu
        self.__start_menu.set_app(self)
        self.__settings = settings
        self.__orm = ORM(self.__settings)

    @property
    def settings(self) -> Settings:
        """
        Возвращает подключенные настройки.

        :return: Settings.
        """
        return self.__settings

    @property
    def orm(self) -> ORM:
        """
        Возвращает инструмент для работы с базой данных.

        :return: Инструмент для работы с базой данных.
        """
        return self.__orm

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
