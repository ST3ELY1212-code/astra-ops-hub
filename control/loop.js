const crypto = require("crypto");
const WRITE = new Set(["crm_write","refund","email_send","email_provision","infra_change","contract_sign","payment_capture","production_deploy","phi_export"]);
const BLOCKED = new Set(["clinical_decision","unrestricted_root"]);
const READ = new Set(["read_logs","page_oncall","research","analyze","draft"]);
const KNOWN = new Set([...WRITE, ...BLOCKED, ...READ]);
const state = globalThis.__astraState || (globalThis.__astraState = { events: [], tickets: {}, workers: {}, observations: {}, proposals: {} });
function now() { return new Date(); }
function emit(kind, payload, runId) {
  const ev = { id: crypto.randomUUID(), ts: now().toISOString(), kind, run_id: runId || crypto.randomUUID(), payload };
  state.events.push(ev);
  if (state.events.length > 500) state.events.splice(0, state.events.length - 500);
  return ev;
}
function heartbeat(id, role) { state.workers[id] = { id, role, last_seen: now().toISOString() }; }
function workerSnapshot() {
  const live = [], stale = [], t = now();
  for (const rec of Object.values(state.workers)) {
    const age = (t - new Date(rec.last_seen)) / 1000;
    (age > 120 ? stale : live).push({ ...rec, age_s: age });
  }
  return { live, stale, healthy: stale.length === 0, stale_after_s: 120 };
}
function expireTickets() {
  const expired = [], t = now();
  for (const ticket of Object.values(state.tickets)) {
    if (ticket.status === "open" && new Date(ticket.expires_at) < t) { ticket.status = "expired"; expired.push(ticket.id); }
  }
  return expired;
}
function tick() {
  emit("tick", { source: "vercel-cron" });
  heartbeat("vercel-tick", "scheduler");
  const expired = expireTickets();
  const workers = workerSnapshot();
  const investigations = Object.values(state.observations).filter((o) => o.status === "investigate");
  const snap = {
    healthy: workers.healthy,
    workers,
    expired_approvals: expired,
    open_approvals: Object.values(state.tickets).filter((t) => t.status === "open"),
    investigations,
    recent_events: state.events.slice(-20).map((e) => ({ kind: e.kind, ts: e.ts, run_id: e.run_id })),
    directive: "Three observations start investigation. They do not authorize a code change."
  };
  emit("tick_complete", { expired: expired.length, investigate: investigations.length });
  return snap;
}
function health() {
  heartbeat("vercel-health", "edge");
  return { ok: true, workers: workerSnapshot(), events: state.events.length, tickets: Object.keys(state.tickets).length };
}
function approve({ ticket_id, action, case_id }) {
  const ticket = state.tickets[ticket_id];
  if (!ticket) return { allowed: false, reason: "unknown_ticket" };
  if (ticket.status !== "open") return { allowed: false, reason: "ticket_" + ticket.status };
  if (ticket.action !== action || ticket.case_id !== case_id) return { allowed: false, reason: "scope_mismatch" };
  if (new Date(ticket.expires_at) < now()) { ticket.status = "expired"; return { allowed: false, reason: "expired" }; }
  ticket.status = "consumed"; ticket.consumed_at = now().toISOString();
  emit("approval_consumed", { ticket_id, action, case_id });
  return { allowed: true, reason: "consumed", ticket };
}
module.exports = { tick, health, approve, emit, state };
