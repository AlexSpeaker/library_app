from typing import Optional

from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import get_id, get_not_empty_string, get_year
from core.menu import book_manage_menu


@book_manage_menu.mark(name="Добавить книгу")
def add_book_category(app: Library) -> None:
    """
    Пользователь вводит title, author и year,
    после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.

    :param app: Экземпляр класса Library.
    :return: None
    """
    title = get_not_empty_string("Введите название книги: ")
    author = get_not_empty_string("Ведите автора: ")
    year = get_year("Введите год выпуска книги: ")
    book = Book(title=title, author=author, year=int(year))
    app.orm.add(book)
    print("Готово.")


@book_manage_menu.mark(name="Удалить книгу")
def delete_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    while True:
        user_choice = input(
            f"Вы действительно хотите удалить книгу '{book.title}' (N/y): "
        )
        if user_choice.lower() == "y" or user_choice.lower() == "n":
            break
    if user_choice.lower() == "n":
        return

    app.orm.delete(book)
    print("Книга '{}' была успешно удалена.".format(book.title))


@book_manage_menu.mark(name="Выдать книгу читателю")
def give_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    elif not book.status:
        print("Ошибка! Книга '{}' ранее уже была выдана читателю.".format(book.title))
        return
    book.status = False
    app.orm.update(book)
    print("Книга '{}' была успешно выдана читателю.".format(book.title))


@book_manage_menu.mark(name="Принять книгу")
def accept_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    elif book.status:
        print(
            "Ошибка! Книга '{}' ранее уже была возвращена в библиотеку.".format(
                book.title
            )
        )
        return
    book.status = True
    app.orm.update(book)
    print("Книга '{}' была успешно возвращена в библиотеку.".format(book.title))


@book_manage_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
