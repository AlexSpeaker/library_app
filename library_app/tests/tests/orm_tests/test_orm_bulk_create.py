import pytest
from core.db_models.author import Author
from core.orm.classes.orm import ORM
from settings.settings_class import Settings
from tests.tests.utils import get_db_data


@pytest.mark.orm
def test_orm_bulk_create(orm_no_data: ORM, settings: Settings) -> None:
    """
    Проверим массовое создание моделей.
    :param orm_no_data: ORM с пустой базой.
    :param settings: Настройки.
    :return: None.
    """

    # Убедимся, что база данных пустая.
    db = get_db_data(settings)
    assert len(db) == 0

    # Создадим модели и сохраним их через метод bulk_create.
    author_1 = Author(first_name="Николай", last_name="Носов")
    author_2 = Author(first_name="Михаил", last_name="Булгаков")
    author_3 = Author(first_name="Сергей", last_name="Есенин")
    orm_no_data.bulk_create(author_1, author_2, author_3)

    # Проверим записи в БД.
    db = get_db_data(settings)
    assert len(db) > 0
    assert {author_1.last_name, author_2.last_name, author_3.last_name} == {
        data["last_name"] for data in db["authors"]
    }
