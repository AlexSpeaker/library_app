from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    title: str
    author: str
    year: int
    status: bool = True  # True - в наличии, False - выдана
    id: Optional[int] = None
