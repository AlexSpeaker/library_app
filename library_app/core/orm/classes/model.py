from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class BaseModel:

    def looks_like_strictly(self, **kwargs: str | int | bool) -> bool:
        return all(
            (
                getattr(self, key).lower() == value.lower()
                if isinstance(value, str)
                else getattr(self, key) == value
            )
            for key, value in kwargs.items()
        )

    def looks_like_softly(self, **kwargs: str | int | bool) -> bool:
        return all(
            (
                getattr(self, key).lower().startswith(value.lower())
                if isinstance(value, str)
                else getattr(self, key) == value
            )
            for key, value in kwargs.items()
        )

    def to_dict(self) -> Dict[str, Any]:
        # Почему-то у меня тут pycharm подсвечивает self, хотя у mypy вопросов нет.
        return {
            key: value
            for key, value in asdict(self).items()
            if not key.startswith("__")
        }
