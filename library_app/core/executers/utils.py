import re
from datetime import datetime
from typing import Any, List, Optional, Sequence

from core.classes.app import Library
from core.db_models.author import Author
from core.db_models.book import Book


def get_not_empty_string(msg: str) -> str:
    """
    Функция строго следит, что бы пользователь хоть что-то ввёл.

    :param msg: Приглашение к вводу.
    :return: То, что введёт пользователь.
    """
    while True:
        user_input = input(msg)
        if user_input:
            break
        print("---> Поле не может быть пустым.")
    return user_input


def get_id(msg: str) -> str:
    """
    Функция строго следит, что бы пользователь ввёл число.

    :param msg: Приглашение к вводу.
    :return: То, что введёт пользователь.
    """
    while True:
        user_input = get_not_empty_string(msg)
        if user_input.isdigit():
            break
        print("---> ID должно быть числом.")
    return user_input


def get_year(msg: str) -> str:
    """
    Функция строго следит, что бы пользователь ввёл год формата YYYY, где Y это цифра.
    А так же, чтобы год был от 1000 до (год запуска пользователем программы).

    :param msg: Приглашение к вводу.
    :return: То, что введёт пользователь.
    """
    pattern = r"^\d\d\d\d$"
    while True:
        user_input = input(msg)
        if not re.match(pattern, user_input):
            print("---> Год должен быть формата YYYY, где Y это цифра.")
            continue
        elif int(user_input) > datetime.now().year or int(user_input) < 1000:
            print(f"---> Год должен быть от 1000 до {datetime.now().year}")
            continue
        break
    return user_input


class Table:
    """Класс для таблиц."""

    def __init__(self, data: Sequence[Sequence[Any]], columns: Sequence[str]) -> None:
        """
        Инициализация класса.
        :param data: Данные для печати.
            Количество данных в каждой последовательности должно быть равно количеству столбцов.
        :param columns: Название столбцов.
        """
        for item_data in data:
            if len(item_data) != len(columns):
                raise ValueError(
                    "Количество передаваемых данных для строки не равно количеству столбцов."
                )
        self.__data_sequence = data
        self.__columns = columns
        self.__size_columns = self.__get_size_columns()
        self.__number_partitions = len(columns) + 1
        self.__width_all_table = sum(self.__size_columns) + self.__number_partitions

    def __get_size_columns(self) -> List[int]:
        """
        Вернёт список из размеров столбцов (по порядку),
        размер определяется по максимальному контенту столбца.
        :return: None.
        """
        size_columns = [len(col) for col in self.__columns]
        for i in range(len(self.__columns)):
            size_column = max((len(str(data[i])) + 4) for data in self.__data_sequence)
            if size_columns[i] < size_column:
                size_columns[i] = size_column
        return size_columns

    def __print_header(self) -> None:
        """
        Печать шапки таблицы. Названия столбцов.
        :return: None.
        """
        print("-" * self.__width_all_table)
        print("|", end="")
        for column, size_column in zip(self.__columns, self.__size_columns):
            print("{:^{size_column}}|".format(column, size_column=size_column), end="")
        print()
        print("-" * self.__width_all_table)

    def __print_body(self) -> None:
        """
        Печатает все полезные данные таблицы.

        :return: None.
        """
        for data in self.__data_sequence:
            print("|", end="")
            for value, size_column in zip(data, self.__size_columns):
                print(
                    "{:^{size_column}}|".format(value, size_column=size_column), end=""
                )
            print()
            print("-" * self.__width_all_table)

    def __print_footer(self) -> None:
        """
        Печать 'подвала' таблицы.

        :return: None.
        """

    def show(self) -> None:
        """
        Покажет красивую таблицу.

        :return: None.
        """
        self.__print_header()
        self.__print_body()
        self.__print_footer()


def get_data_books_for_table(books: Sequence[Book], app: Library) -> List[List[str]]:
    """
    Преобразует последовательность из книг в данные для таблицы.

    :param books: Последовательность из книг.
    :param app: Экземпляр приложения Library.
    :return: Данные для таблицы.
    """
    data_list = []
    for book in books:
        if book.author_id:
            author: Optional[Author] = app.orm.select(Author).get(book.author_id)
            if author:
                author_name = " ".join([author.first_name, author.last_name])
            else:
                author_name = str(book.author_id)
        else:
            raise ValueError(f"У книги {book.title} неожиданно отсутствует author_id")
        data = [str(book.id), book.title, author_name, str(book.year), book.status_str]
        data_list.append(data)
    return data_list
