from typing import Any, Dict, List, Optional, Tuple


class QuerySet:
    """Класс QuerySet"""
    def __init__(self, model: Any, database: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Инициализация класса.
        :param model: Модель.
        :param database: Словарь.
        """
        self.__model = model
        self.__table_name = model.__tablename__
        self.__database = database.setdefault(self.__table_name, [])
        self.__queryset = (self.__model(**data) for data in self.__database)

    def all(self) -> Tuple[Any, ...]:
        """
        Функция вернёт все записи (на основании переданной модели)
        упакованные в переданную модель.

        :return: Кортеж из экземпляров переданной модели.
        """
        return tuple(self.__queryset)

    def filter_soft(self, **kwargs: Any) -> Tuple[Any, ...]:
        """
        Функция отфильтрует записи от всех записей (на основании переданной модели),
        применяя мягкую фильтрацию.

        :param kwargs: Словарь с данными фильтрации.
        :return: Кортеж из экземпляров переданной модели.
        """
        return tuple(
            filter(lambda model: model.looks_like_softly(**kwargs), self.__queryset)
        )

    def filter_strict(self, **kwargs: Any) -> Tuple[Any, ...]:
        """
        Функция отфильтрует записи от всех записей (на основании переданной модели),
        применяя строгую фильтрацию.

        :param kwargs: Словарь с данными фильтрации.
        :return: Кортеж из экземпляров переданной модели.
        """
        return tuple(
            filter(lambda model: model.looks_like_strictly(**kwargs), self.__queryset)
        )

    def get(self, pk: int) -> Optional[Any]:
        """
        Функция попробует найти конкретную запись на основании переданного id.

        :param pk: Id модели.
        :return: Экземпляр Модели, если такая запись есть, иначе None.
        """
        model = tuple(filter(lambda m: m.looks_like_strictly(id=pk), self.__queryset))
        if model:
            return model[0]
        return None
