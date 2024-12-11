from dataclasses import dataclass
from typing import Optional

from core.orm.classes.model import BaseModel


@dataclass
class Author(BaseModel):
    """
    Модель автора.

    **id** - Id автора. \n
    **first_name** - Имя автора. \n
    **last_name** - Фамилия автора. \n
    """

    __tablename__ = "authors"

    first_name: str
    last_name: str
    id: Optional[int] = None
