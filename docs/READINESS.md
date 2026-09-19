# Readiness (operator)

Not-ready is the trigger to keep building. Do not ask for permission to make readiness changes.

## Locked policy
- Deny unknown MCP actions
- Tickets, not booleans
- Three observations start investigation only (do not authorize a code change)
- Clinical blocked
- No live Kalshi orders
- Do not activate code/policy change from repetition alone

## Apex observability
`GET /api/health` and `/api/tick` report:
- `deploy.deploy_sha` — Vercel git SHA when present
- `deploy.control_revision` / `control_sha_hint` — last intentional control plane pin
- `deploy.split` — true when deploy tip does not match control pin
- `state_line` — one-line STATE for email/app without opening GitHub

## Vercel Hobby note
Cron must be **once per day** on Hobby (`0 14 * * *` UTC). The outer-loop agent still probes `/api/health` / `/api/tick` on its own schedule; Vercel cron is a backup tick only. Upgrade to Pro to restore sub-daily crons.

## Still blocking paper Kalshi path
1. Push clean Fiveplane source to `ST3ELY1212-code/Kalshi_BetBot` (no secrets/node_modules/zip).
2. Paper runner (no live orders) wired against open 15m crypto markets.
3. Astra apex shows healthy workers and no stale/expired-approval pile-up.

## Spiral note
Progress is layered. Do not only re-run idle heartbeats; each pass should add observability, close a gate, or shrink tip/control drift.
