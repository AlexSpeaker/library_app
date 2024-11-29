from typing import Any, Dict, List, Optional, Tuple


class QuerySet:
    def __init__(self, model: Any, database: Dict[str, List[Dict[str, Any]]]) -> None:
        self.__model = model
        self.__table_name = model.__tablename__
        self.__database = database.setdefault(self.__table_name, [])
        self.__queryset = (self.__model(**data) for data in self.__database)

    def all(self) -> Tuple[Any, ...]:
        return tuple(self.__queryset)

    def filter_soft(self, **kwargs: Any) -> Tuple[Any, ...]:
        return tuple(
            filter(lambda model: model.looks_like_softly(**kwargs), self.__queryset)
        )

    def filter_strict(self, **kwargs: Any) -> Tuple[Any, ...]:
        return tuple(
            filter(lambda model: model.looks_like_strictly(**kwargs), self.__queryset)
        )

    def get(self, pk: int) -> Optional[Any]:
        model = tuple(filter(lambda m: m.looks_like_strictly(id=pk), self.__queryset))
        if model:
            return model[0]
        return None
