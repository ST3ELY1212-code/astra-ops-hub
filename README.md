# Astra Ops Hub

Nineteen **runnable** business engines that implement the GPT-6 Astra workflow cases from the beamnxw field guide, plus an MCP server, memory evolution log, and approval policy.

This is not a prompt pack. Each case executes against the Northlamp Commerce world fixture, returns a structured artifact, splits **evidence vs assumption**, and refuses unsafe writes until a human approves.

Repo: https://github.com/ST3ELY1212-code/astra-ops-hub

## Install

```bash
git clone https://github.com/ST3ELY1212-code/astra-ops-hub.git
cd astra-ops-hub
python -m pip install -e .
python -m pytest -q
```

## CLI

```bash
python -m astra_ops.cli list
python -m astra_ops.cli run support_resolver
python -m astra_ops.cli run multi_agent --goal "founder week pack"
python -m astra_ops.cli run-all
python -m astra_ops.cli monitor
python -m astra_ops.cli memory
python -m astra_ops.cli focus
```

## MCP

```json
{
  "mcpServers": {
    "astra-ops-hub": {
      "command": "python",
      "args": ["-m", "astra_ops.mcp_server"],
      "cwd": "/absolute/path/to/astra-ops-hub"
    }
  }
}
```

Tools: list_cases, run_case, run_all, monitor, memory_recent, focus_directives.

Open site/index.html for the operator console.
