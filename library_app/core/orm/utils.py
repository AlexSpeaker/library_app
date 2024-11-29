from typing import Any, Dict


def get_next_id(db: Dict[str, Dict[str, Any]]) -> int:
    keys = db.keys()
    if not keys:
        new_id = 1
    else:
        new_id = max(int(id_book) for id_book in keys) + 1
    return new_id
