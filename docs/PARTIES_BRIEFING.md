# Parties briefing (Astra pointer)

Full briefing lives in the Kalshi session home:

https://github.com/ST3ELY1212-code/Kalshi_ImprovementLoop/blob/main/docs/PARTIES_BRIEFING.md

Do not copy PaperDesk artifacts into this repo.

## Locked MCP directive (this session)

```
Deny unknown actions.
Never treat a boolean as approval. Consume a ticket whose action, case_id, and expiry match.
Call tick before planning.
Call replay(run_id) after a crash or retry; do not rerun completed activities.
If an observation count reaches 3, open an investigation proposal. Do not activate it.
Activation requires evaluate(passed=true) plus an explicit activate call.
Clinical decisions stay blocked.
```

## This application's job

Nineteen deterministic engines + MCP + approval policy. Grok owns business truth. Vercel `/api/tick` is the cheap outer loop (on Hobby, the **hourly** Grok job `astra-ops-tick` is the actual clock — `*/15` cron does not run). ChatGPT Temporal owns crash-replay of long tools. Three identical observations open an investigation only.

Health host: `https://astra-ops-hub.vercel.app/api/health` (apex). Team hostname is SSO-gated.

Hermes mirrors Grokbot on the Kalshi repo (`paperdesk/public/hermes/`), not here.
