from typing import Optional, Tuple

from core.classes.app import Library
from core.classes.menu import MenuExit
from core.db_models.author import Author
from core.db_models.book import Book
from core.executers.utils import get_id, get_not_empty_string, get_year
from core.menu import book_manage_menu


@book_manage_menu.mark(name="Добавить книгу")
def add_book_category(app: Library) -> None:
    """
    Пользователь вводит title, author и year,
    после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    title = get_not_empty_string("Введите название книги (--exit для выхода): ")
    author = get_not_empty_string(
        "Ведите автора (ввод должен быть Имя Фамилия) (--exit для выхода): "
    )
    year = get_year("Введите год выпуска книги (--exit для выхода): ")
    author_info = author.split(" ")
    first_name, last_name = (
        (author_info[0], author_info[1])
        if len(author_info) == 2
        else ("", author_info[0])
    )
    author_obj: Tuple[Author, ...] = app.orm.select(Author).filter_strict(
        first_name=first_name, last_name=last_name
    )

    author_bd: Author = (
        app.orm.add(Author(first_name=first_name, last_name=last_name))
        if not author_obj
        else author_obj[0]
    )
    book = Book(title=title, year=int(year), author_id=author_bd.id)
    app.orm.add(book)
    print("Готово.")


@book_manage_menu.mark(name="Удалить книгу")
def delete_book_category(app: Library) -> None:
    """
    Пользователь вводит id книги и функция её удаляет, если она существует,
    иначе функция сообщит, что такой книги нет и ничего не произойдёт.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    id_book = get_id("Введите id книги (--exit для выхода): ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print(f"Ошибка! Книга с ID={id_book} не существует.")
        return
    while True:
        user_choice = input(
            f"Вы действительно хотите удалить книгу '{book.title}' (N/y): "
        )
        if (
            user_choice.lower() == "y"
            or user_choice.lower() == "n"
            or user_choice.lower().strip() == ""
        ):
            break
    if user_choice.lower() == "n" or user_choice.lower().strip() == "":
        return

    app.orm.delete(book)
    print(f"Книга '{book.title}' была успешно удалена.")


@book_manage_menu.mark(name="Выдать книгу читателю")
def give_book_category(app: Library) -> None:
    """
    Пользователь вводит id книги и функция её пометит как 'выдана', если она существует,
    иначе функция сообщит, что такой книги нет и ничего не произойдёт.
    Если книга уже была выдана, то функция также сообщит об этом.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    id_book = get_id("Введите id книги (--exit для выхода): ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print(f"Ошибка! Книга с ID={id_book} не существует.")
        return
    elif not book.status:
        print(f"Ошибка! Книга '{book.title}' ранее уже была выдана читателю.")
        return
    book.status = False
    app.orm.update(book)
    print(f"Книга '{book.title}' была успешно выдана читателю.")


@book_manage_menu.mark(name="Принять книгу")
def accept_book_category(app: Library) -> None:
    """
    Пользователь вводит id книги и функция её пометит как 'в наличии', если она существует,
    иначе функция сообщит, что такой книги нет и ничего не произойдёт.
    Если книга уже была в наличии, то функция также сообщит об этом.

    :param app: Экземпляр класса Library.
    :return: None.
    """
    id_book = get_id("Введите id книги (--exit для выхода): ")
    book: Optional[Book] = app.orm.select(Book).get(int(id_book))
    if not book:
        print(f"Ошибка! Книга с ID={id_book} не существует.")
        return
    elif book.status:
        print(f"Ошибка! Книга '{book.title}' ранее уже была возвращена в библиотеку.")
        return
    book.status = True
    app.orm.update(book)
    print(f"Книга '{book.title}' была успешно возвращена в библиотеку.")


@book_manage_menu.mark(name="<-- Назад")
def exit_category() -> None:
    """
    Функция выхода из меню.

    :return: None.
    """
    raise MenuExit
