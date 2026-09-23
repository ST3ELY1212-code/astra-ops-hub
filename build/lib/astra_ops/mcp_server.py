"""Minimal MCP stdio server for Astra Ops Hub."""
from __future__ import annotations
import json, sys
from astra_ops.engines import ENGINES
from astra_ops.memory import focus_directives, recent
from astra_ops.orchestrator import monitor_snapshot, run_all, run_case

TOOLS = [
    {"name": "list_cases", "description": "List the 19 Astra Ops Hub use-case engines", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "run_case", "description": "Execute one use-case engine against the Northlamp world fixture", "inputSchema": {"type": "object", "properties": {"case_id": {"type": "string", "enum": list(ENGINES)}, "goal": {"type": "string"}}, "required": ["case_id"]}},
    {"name": "run_all", "description": "Execute every engine and record memory plus focus areas", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "monitor", "description": "Heartbeat: statuses and open approval gates", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "memory_recent", "description": "Read evolution memory", "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer"}}}},
    {"name": "focus_directives", "description": "Directives learned from competitor gaps", "inputSchema": {"type": "object", "properties": {"case_id": {"type": "string"}}}},
]

def _handle(name: str, args: dict) -> dict:
    if name == "list_cases":
        return {"cases": list(ENGINES)}
    if name == "run_case":
        return run_case(args["case_id"], {"goal": args.get("goal", "")})
    if name == "run_all":
        return {"results": run_all()}
    if name == "monitor":
        return monitor_snapshot()
    if name == "memory_recent":
        return {"memory": recent(args.get("limit", 40))}
    if name == "focus_directives":
        return {"directives": focus_directives(args.get("case_id"))}
    raise ValueError(name)

def _reply(msg_id, result=None, error=None):
    body = {"jsonrpc": "2.0", "id": msg_id}
    if error:
        body["error"] = error
    else:
        body["result"] = result
    sys.stdout.write(json.dumps(body) + "\n")
    sys.stdout.flush()

def main() -> None:
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        msg = json.loads(raw)
        method = msg.get("method")
        msg_id = msg.get("id")
        if method == "initialize":
            _reply(msg_id, {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "astra-ops-hub", "version": "1.0.0"}})
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            _reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = msg.get("params") or {}
            try:
                result = _handle(params["name"], params.get("arguments") or {})
                _reply(msg_id, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}], "isError": False})
            except Exception as exc:
                _reply(msg_id, {"content": [{"type": "text", "text": str(exc)}], "isError": True})
        elif method == "ping":
            _reply(msg_id, {})
        elif msg_id is not None:
            _reply(msg_id, error={"code": -32601, "message": f"unknown method {method}"})

if __name__ == "__main__":
    main()
