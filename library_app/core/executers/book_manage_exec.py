from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.book import Book
from core.executers.utils import get_id, get_not_empty_string, get_year
from core.menu import book_manage_menu
from core.orm.classes import ORMException


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
    book = Book(title=title, author=author, year=year)
    app.orm.add_book(book)
    print("Готово.")


@book_manage_menu.mark(name="Удалить книгу")
def delete_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    try:
        book = app.orm.get_book(id_book)
    except ORMException:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    while True:
        user_choice = input(f"Вы действительно хотите удалить книгу '{book.title}' (N/y): ")
        if user_choice.lower() == "y":
            break
        elif not user_choice:
            return
    app.orm.delete_book(book)
    print("Книга '{}' была успешно удалена.".format(book.title))


@book_manage_menu.mark(name="Выдать книгу читателю")
def give_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    try:
        book = app.orm.get_book(id_book)
    except ORMException:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    if not book.status:
        print("Ошибка! Книга '{}' ранее уже была выдана читателю.".format(book.title))
        return
    book.status = False
    app.orm.update_book(book)
    print("Книга '{}' была успешно выдана читателю.".format(book.title))


@book_manage_menu.mark(name="Принять книгу")
def accept_book_category(app: Library) -> None:
    id_book = get_id("Введите id книги: ")
    try:
        book = app.orm.get_book(id_book)
    except ORMException:
        print("Ошибка! Книга с ID={} не существует.".format(id_book))
        return
    if book.status:
        print("Ошибка! Книга '{}' ранее уже была возвращена в библиотеку.".format(book.title))
        return
    book.status = True
    app.orm.update_book(book)
    print("Книга '{}' была успешно возвращена в библиотеку.".format(book.title))


@book_manage_menu.mark(name="<-- Назад")
def exit_category() -> None:
    raise MenuExit
