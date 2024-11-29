import re
from datetime import datetime
from typing import Any, List, Sequence


def get_not_empty_string(msg: str) -> str:
    while True:
        user_input = input(msg)
        if user_input:
            break
        print("---> Поле не может быть пустым.")
    return user_input


def get_id(msg: str) -> str:
    while True:
        user_input = get_not_empty_string(msg)
        if user_input.isdigit():
            break
        print("---> ID должно быть числом.")
    return user_input


def get_year(msg: str) -> str:
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
    def __init__(self, objects: Sequence[Any], columns: Sequence[str]) -> None:
        self.__objects = objects
        self.__columns = columns
        self.__size_columns = self.__get_size_columns()
        self.__number_partitions = len(columns) + 1
        self.__width_all_table = sum(self.__size_columns) + self.__number_partitions

    def __print_header(self) -> None:
        print("-" * self.__width_all_table)
        print("|", end="")
        for column, size_column in zip(self.__columns, self.__size_columns):
            print("{:^{size_column}}|".format(column, size_column=size_column), end="")
        print()
        print("-" * self.__width_all_table)

    def __print_body(self) -> None:
        for obj in self.__objects:
            print("|", end="")
            for column, size_column in zip(self.__columns, self.__size_columns):
                value = self.__get_obj_value(obj, column)
                print(
                    "{:^{size_column}}|".format(value, size_column=size_column), end=""
                )
            print()
            print("-" * self.__width_all_table)

    @staticmethod
    def __get_obj_value(obj: Any, name: str) -> Any:
        value = getattr(obj, name)
        if isinstance(value, bool):
            try:
                value_str = getattr(obj, f"{name}_str")
            except AttributeError:
                pass
            else:
                value = value_str
        return value

    def __print_footer(self) -> None:
        pass

    def __get_size_columns(self) -> List[int]:
        size_columns = []
        for col in self.__columns:
            size_column = max(
                (len(str(self.__get_obj_value(obj, col))) + 4) for obj in self.__objects
            )
            size_columns.append(size_column)
        return size_columns

    def show(self) -> None:
        self.__print_header()
        self.__print_body()
        self.__print_footer()
