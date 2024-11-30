import json
from typing import Any, Dict

from settings.settings_class import Settings


def get_db_data(settings: Settings) -> Dict[str, Any]:
    """
    Функция читает БД из файла и возвращает её в виде словаря.
    :param settings: Настройки.
    :return:
    """
    db_path = settings.db_settings.db_base_path / settings.db_settings.name
    with open(db_path, "r", encoding="utf-8") as file:
        db: Dict[str, Any] = json.load(file)
    return db
