import json
from pathlib import Path
from typing import Dict

from settings.settings_class import Settings


def get_database(settings: Settings) -> Dict[str, str | int | bool]:
    db_dir: Path = settings.db_settings.db_base_path
    db_name: str = settings.db_settings.name
    db_path: Path = db_dir / db_name
    with open(db_path, "r", encoding="utf-8") as file:
        db = json.load(file)
    if not isinstance(db, dict):
        raise ValueError("Загруженные данные не являются словарем.")
    return db


# def get_all_books()
