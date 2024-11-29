import json
from pathlib import Path
from typing import Any, Dict, List

from core.orm.classes.queryset import QuerySet
from settings.settings_class import Settings


class BaseORM:
    """Базовый класс ORM"""

    def __init__(self, settings: Settings):
        """
        Инициализация класса.
        :param settings: Подключаемые настройки.
        """
        self.__settings: Settings = settings
        db_dir: Path = settings.db_settings.db_base_path
        db_name: str = settings.db_settings.name
        self.__db_path: Path = db_dir / db_name

    def _get_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Функция получит json из файла и вернёт его в виде словаря.

        :return: Словарь.
        """
        with open(self.__db_path, "r", encoding="utf-8") as file:
            db = json.load(file)
        if not isinstance(db, dict):
            raise ValueError("Загруженные данные не являются словарем.")
        return db

    def _save_db(self, db: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Функция принимает словарь и записывает его в файл как json объект.

        :param db:
        :return:
        """
        with open(self.__db_path, "w", encoding="utf-8") as file:
            json.dump(
                db, file, ensure_ascii=False, indent=4
            )  # Почему-то у меня тут pycharm подсвечивает file, хотя у mypy вопросов нет.


class ORM(BaseORM):
    """Класс ORM"""

    def __init__(self, settings: Settings):
        """
        Инициализация класса.
        :param settings: Подключаемые настройки.
        """
        super().__init__(settings)

    def select(self, model: Any) -> QuerySet:
        """
        Функция принимает модель, передает его и базу данных классу QuerySet.
        Возвращает Экземпляр класса QuerySet.

        :param model: Модель.
        :return: Экземпляр класса QuerySet.
        """
        return QuerySet(model, self._get_database())

    def add(self, model: Any) -> Any:
        """
        Функция принимает модель и записывает её в базу данных.

        :param model: Модель.
        :return: Вернёт модель с id.
        """
        db = self._get_database()
        table_name = model.__tablename__
        db.setdefault(table_name, [])
        new_id = max(m["id"] for m in db[table_name]) + 1 if db[table_name] else 1
        model.id = new_id
        db[table_name].append(model.to_dict())
        self._save_db(db)
        return model

    def delete(self, model: Any) -> None:
        """
        Функция принимает модель, находит её в бд по id и удаляет её.

        :param model: Модель.
        :return: None.
        """
        db = self._get_database()
        table_name = model.__tablename__
        table = db.setdefault(table_name, [])
        db[table_name] = [dict(**data) for data in table if data["id"] != model.id]
        self._save_db(db)

    def update(self, model: Any) -> None:
        """
        Функция принимает модель, находит её в бд по id и обновляет данные.

        :param model: Модель.
        :return: None.
        """
        db = self._get_database()
        table_name = model.__tablename__
        table = db.setdefault(table_name, [])
        for item in table:
            if item["id"] == model.id:
                item.update(model.to_dict())
                break
        self._save_db(db)
