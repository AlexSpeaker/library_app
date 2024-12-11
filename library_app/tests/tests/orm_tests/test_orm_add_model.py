import pytest
from core.db_models.author import Author
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_add_model(orm_no_data: ORM, settings: Settings) -> None:
    """
    Проверим создание модели.

    :param orm_no_data: ORM с пустой базой.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что база данных пустая.
    db = get_db_data(settings)
    assert len(db) == 0

    # Создадим модель и проверим её в БД.
    author_1 = Author(first_name="Николай", last_name="Носов")
    orm_no_data.add(author_1)
    assert author_1.id is not None

    # Убедимся, что запись есть в БД.
    db = get_db_data(settings)
    assert len(db["authors"]) > 0
    assert db["authors"][0]["id"] == author_1.id
    assert db["authors"][0]["first_name"] == author_1.first_name
    assert db["authors"][0]["last_name"] == author_1.last_name
