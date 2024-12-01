import json
from typing import Dict


def load_json_db(json_path: str) -> Dict[str, Dict]:
    with open(json_path, "r", encoding="utf-8") as disk_lib:
        return json.loads(disk_lib.read())


def dump_json_db(json_path: str, data: Dict[str, Dict]) -> None:
    with open(json_path, "w", encoding="utf-8") as disk_lib:
        disk_lib.write(json.dumps(data, sort_keys=True))
