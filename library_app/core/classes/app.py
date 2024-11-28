from core.classes.menu import Menu

class AppExit(Exception):
    """Исключение, для выхода из программы."""

class Library:
    """Класс приложения."""

    def __init__(self, start_menu: Menu):
        """Инициализация класса."""
        self.__start_menu = start_menu

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
