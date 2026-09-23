from __future__ import annotations

from astra_ops.engines import ENGINES
from astra_ops.memory import focus_directives, log_run, remember


def run_case(case_id: str, payload: dict | None = None, remember_run: bool = True) -> dict:
    if case_id not in ENGINES:
        raise KeyError(f"unknown case {case_id}")
    result = ENGINES[case_id](payload or {})
    result["memory_directives"] = focus_directives(case_id)
    if remember_run:
        log_run(result)
        remember(case_id, "run", f"status={result['status']}")
    return result


def run_all(remember_run: bool = True) -> list[dict]:
    out = []
    for case_id in ENGINES:
        if case_id == "multi_agent":
            continue
        out.append(run_case(case_id, remember_run=remember_run))
    out.append(run_case("multi_agent", remember_run=remember_run))
    return out


def monitor_snapshot() -> dict:
    """What an MCP heartbeat would report."""
    results = run_all(remember_run=False)
    return {
        "healthy": all(r["status"] in {"completed", "needs_approval", "blocked"} for r in results),
        "by_status": {
            "completed": [r["case_id"] for r in results if r["status"] == "completed"],
            "needs_approval": [r["case_id"] for r in results if r["status"] == "needs_approval"],
            "blocked": [r["case_id"] for r in results if r["status"] == "blocked"],
        },
        "open_approvals": sorted({a for r in results for a in r.get("approval_required", [])}),
    }
