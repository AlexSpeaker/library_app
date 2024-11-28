from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataBaseSettings:
    db_base_path: Path = Path(__file__).parent.parent / "database"


@dataclass(frozen=True)
class Settings:
    base_path: Path = Path(__file__).parent.parent
    db_settings: DataBaseSettings = DataBaseSettings()
