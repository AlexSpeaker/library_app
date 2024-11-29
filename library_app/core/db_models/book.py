from dataclasses import dataclass
from typing import Optional

from core.orm.classes.model import BaseModel


@dataclass
class Book(BaseModel):
    """
    Модель книги.

    **id** - Id книги. \n
    **title** - Название книги. \n
    **author** - Автор книги. \n
    **year** - Год издания. \n
    **status** - Статус книги: “в наличии (True)”, “выдана (False)”.
    """

    __tablename__ = "book"

    title: str
    author: str
    year: int
    status: bool = True  # True - в наличии, False - выдана
    id: Optional[int] = None

    @property
    def status_str(self) -> str:
        return "В наличии" if self.status else "Выдана"
