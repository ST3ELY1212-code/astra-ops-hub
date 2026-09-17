"""Append-only JSONL store. Rebuild in memory."""
from __future__ import annotations
import json
from pathlib import Path

BASE = Path("/tmp/astra-ops-hub")
BASE.mkdir(parents=True, exist_ok=True)

def path(name: str) -> Path:
    p = BASE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def append(name: str, row: dict) -> None:
    target = path(name)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")

def load_lines(name: str) -> list:
    target = path(name)
    if not target.exists():
        return []
    out = []
    for line in target.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
