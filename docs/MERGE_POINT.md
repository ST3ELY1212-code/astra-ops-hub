# Merge point: Grok control plane + ChatGPT Temporal durability

ChatGPT named four v1 defects. All accepted:
1. Engine module missing from clone.
2. monitor treated fixture labels as liveness.
3. Unknown actions allowed; approval was a caller boolean.
4. Repeated gaps appended clones.

Cycle now: observe → dedupe → propose → evaluate → activate → rollback.
Three observations start an investigation. They do not authorize a patch.

Topology: Python engines stay business truth. Event log + tickets + workers are local durable semantics. Vercel /api/tick is the outer loop. Temporal should wrap MCP tools as activities without changing schemas.
