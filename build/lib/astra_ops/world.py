from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD_PATH = ROOT / "data" / "world.json"


def load_world() -> dict:
    return json.loads(WORLD_PATH.read_text())
