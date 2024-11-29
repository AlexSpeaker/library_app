from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class Book:
    """
    Модель книги.

    **id** - Id книги. \n
    **title** - Название книги. \n
    **author** - Автор книги. \n
    **year** - Год издания. \n
    **status** - Статус книги: “в наличии (True)”, “выдана (False)”.
    """

    title: str
    author: str
    year: str
    status: bool = True  # True - в наличии, False - выдана
    id: Optional[str] = None

    def looks_like(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[str] = None,
    ) -> bool:
        """
        Функция вернёт True при первом совпадении одного из переданных аргументов.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания.
        :return: True при первом совпадении одного из переданных аргументов, иначе False.
        """
        return self.title == title or self.author == author or self.year == year

    def to_dict(self) -> Dict[str, Any]:
        return asdict(
            self
        )  # Почему-то у меня тут pycharm ругается, хотя у mypy вопросов нет.

    @property
    def status_str(self) -> str:
        return "В наличии" if self.status else "Выдана"
