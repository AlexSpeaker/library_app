from pathlib import Path

from settings.settings_class import DataBaseSettings, Settings

base_path = Path(__file__).parent
db_settings = DataBaseSettings(db_base_path=base_path / "database")
test_settings = Settings(base_path=base_path, db_settings=db_settings)
