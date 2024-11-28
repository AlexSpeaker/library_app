from typing import Sequence


def one_line(message: str, width: int) -> None:
    print("*   {:<{width_menu}}*".format(message, width_menu=width))


def print_menu(categories: Sequence[str], title: str) -> None:
    max_word = max(list(categories) + [title], key=len)
    width_menu = len(max_word) + len(str(len(categories))) + 6
    print("*" * (width_menu + 5))
    one_line(title, width_menu)
    one_line("-" * len(title), width_menu)
    for i, category in enumerate(categories, 1):
        one_line(f"{i}. {category}.", width_menu)
    print("*" * (width_menu + 5))
