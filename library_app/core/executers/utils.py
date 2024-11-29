import re
from datetime import datetime


def get_not_empty_string(msg: str) -> str:
    while True:
        user_input = input(msg)
        if user_input:
            break
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
