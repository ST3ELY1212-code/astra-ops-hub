"""Durable memory + evolution log for MCP orchestration."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEM = ROOT / "data" / "memory" / "memory.jsonl"
FOCUS = ROOT / "data" / "memory" / "focus_areas.jsonl"
RUNS = ROOT / "data" / "logs" / "runs.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def remember(case_id: str, kind: str, text: str, extra: dict | None = None) -> dict:
    row = {"ts": _now(), "case_id": case_id, "kind": kind, "text": text, **(extra or {})}
    append(MEM, row)
    return row


def add_focus(case_id: str, gap: str, competitor: str, improvement: str) -> dict:
    row = {
        "ts": _now(),
        "case_id": case_id,
        "competitor_gap": gap,
        "competitor": competitor,
        "directive": improvement,
    }
    append(FOCUS, row)
    remember(case_id, "focus", improvement, {"competitor": competitor})
    return row


def log_run(result: dict) -> None:
    append(RUNS, {"ts": _now(), **{k: result[k] for k in ("case_id", "status") if k in result}, "result": result})
    for area in result.get("focus_areas") or []:
        add_focus(result["case_id"], area.get("gap", ""), area.get("competitor", ""), area.get("improve", area.get("gap", "")))
    for ev in result.get("evidence") or []:
        remember(result["case_id"], "evidence", ev)
    for assump in result.get("assumptions") or []:
        remember(result["case_id"], "assumption", assump)


def recent(limit: int = 40) -> list[dict]:
    if not MEM.exists():
        return []
    lines = MEM.read_text(encoding="utf-8").splitlines()[-limit:]
    return [json.loads(x) for x in lines]


def focus_directives(case_id: str | None = None) -> list[str]:
    if not FOCUS.exists():
        return []
    out = []
    for line in FOCUS.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if case_id and row.get("case_id") != case_id:
            continue
        out.append(row["directive"])
    return out[-20:]
