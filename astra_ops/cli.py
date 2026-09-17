from __future__ import annotations

import argparse
import json
import sys

from astra_ops.engines import ENGINES
from astra_ops.memory import focus_directives, recent
from astra_ops.orchestrator import monitor_snapshot, run_all, run_case


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="astra-ops", description="Astra Ops Hub CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Run one case")
    run.add_argument("case_id", choices=sorted(ENGINES))
    run.add_argument("--goal", default="")
    sub.add_parser("run-all", help="Run every case")
    sub.add_parser("monitor", help="Health + open approvals")
    sub.add_parser("memory", help="Recent memory")
    sub.add_parser("focus", help="Evolution directives")
    sub.add_parser("list", help="List cases")
    args = p.parse_args(argv)

    if args.cmd == "list":
        print("\n".join(ENGINES))
        return 0
    if args.cmd == "run":
        payload = {"goal": args.goal} if args.goal else {}
        print(json.dumps(run_case(args.case_id, payload), indent=2))
        return 0
    if args.cmd == "run-all":
        print(json.dumps(run_all(), indent=2))
        return 0
    if args.cmd == "monitor":
        print(json.dumps(monitor_snapshot(), indent=2))
        return 0
    if args.cmd == "memory":
        print(json.dumps(recent(), indent=2))
        return 0
    if args.cmd == "focus":
        print(json.dumps(focus_directives(), indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
