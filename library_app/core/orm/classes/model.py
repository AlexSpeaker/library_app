from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class BaseModel:
    """Базовый класс модели базы данных"""
    def looks_like_strictly(self, **kwargs: str | int | bool) -> bool:
        """
        Строгое соответствие.
        Вернёт True, если поле модели строго эквивалентно переданному значению.
        Если передаётся несколько значений, то True будет только если все сравнения вернут True.

        :param kwargs: Словарь для сравнения с моделью.
        :return: True или False.
        """
        return all(
            (
                getattr(self, key).lower() == value.lower()
                if isinstance(value, str)
                else getattr(self, key) == value
            )
            for key, value in kwargs.items()
        )

    def looks_like_softly(self, **kwargs: str | int | bool) -> bool:
        """
        Мягкое соответствие.
        Вернёт True, если поле модели начинается с переданного значения.
        Работает только для str, для других типов сравнение строгое.
        Если передаётся несколько значений, то True будет только если все сравнения вернут True.

        :param kwargs: Словарь для сравнения с моделью.
        :return: True или False.
        """
        return all(
            (
                getattr(self, key).lower().startswith(value.lower())
                if isinstance(value, str)
                else getattr(self, key) == value
            )
            for key, value in kwargs.items()
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Конвертирует модель в словарь.

        :return: Словарь.
        """

        # Почему-то у меня тут pycharm подсвечивает self, хотя у mypy вопросов нет.
        return {
            key: value
            for key, value in asdict(self).items()
            if not key.startswith("__")
        }
