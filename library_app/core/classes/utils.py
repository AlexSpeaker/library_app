from typing import Sequence


def one_line(message: str, width: int) -> None:
    """
    Печатает строку меню.

    :param message: Сообщение.
    :param width: Ширина меню.
    :return: None.
    """
    print("*   {:<{width_menu}}*".format(message, width_menu=width))


def print_menu(categories: Sequence[str], title: str) -> None:
    """
    Выводит на экран меню.

    :param categories: Последовательность из категорий.
    :param title: Название меню.
    :return: None.
    """
    max_word = max(list(categories) + [title], key=len)
    width_menu = len(max_word) + len(str(len(categories))) + 6
    print("*" * (width_menu + 5))
    one_line(title, width_menu)
    one_line("-" * len(title), width_menu)
    for i, category in enumerate(categories, 1):
        one_line(f"{i}. {category}.", width_menu)
    print("*" * (width_menu + 5))
