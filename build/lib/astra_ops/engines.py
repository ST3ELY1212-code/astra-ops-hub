from __future__ import annotations

from astra_ops import CASES
from astra_ops.policy import envelope, gate
from astra_ops.world import load_world


def _focus(gap: str, competitor: str = "Lumenoak") -> list[dict]:
    return [{"gap": gap, "competitor": competitor, "improve": gap}]


def computer_agent(payload: dict) -> dict:
    world = load_world()
    employee = next(e for e in world["employees"] if not e.get("onboarding_complete", True))
    return envelope(
        "computer_agent",
        {"employee": employee["name"], "next": ["create_hr_profile", "provision_crm_access"]},
        [f"Onboarding incomplete for {employee['id']}"],
        [],
        [],
        focus_areas=_focus("Automate cross-system onboarding checklist", "Harbor Beam"),
    )


def coding_agent(payload: dict) -> dict:
    world = load_world()
    bug = world["repo_bug"]
    return envelope(
        "coding_agent",
        {
            "patch": "persist_session: avoid overwriting cookie when redis write fails",
            "regression_test": "test_redis_down_keeps_existing_cookie",
            "files": bug["files"],
        },
        [bug["root_cause"]],
        [],
        [],
        focus_areas=_focus("Add resilience pattern for session-store degradation", "Gridwatt"),
    )


def website_qa(payload: dict) -> dict:
    bugs = load_world()["qa_storefront"]["bugs"]
    return envelope(
        "website_qa",
        {"high_severity": [b for b in bugs if b["severity"] == "high"]},
        [f"{len(bugs)} storefront bugs found"],
        [],
        [],
        focus_areas=_focus("Prevent discount and checkout regressions with release gates", "Noxa Home"),
    )


def support_resolver(payload: dict) -> dict:
    world = load_world()
    ticket = world["tickets"][0]
    approval = gate("email_send")
    return envelope(
        "support_resolver",
        {"ticket": ticket["id"], "draft_reply": "Apology, tracking update, and credit offer"},
        ["Ticket linked to delayed enterprise order"],
        [],
        ["email_send"] if approval["status"] == "needs_approval" else [],
        focus_areas=_focus("Reduce response latency for delayed-shipment cases", "Harbor Beam"),
    )


def sales_crm(payload: dict) -> dict:
    lead = load_world()["leads"][0]
    return envelope(
        "sales_crm",
        {"lead_id": lead["id"], "score": 87, "recommended_owner": "s.reid"},
        ["Lead has RFx budget signal"],
        [],
        ["crm_write"],
        focus_areas=_focus("Increase lead routing speed and qualification confidence", "Lumenoak"),
    )


def competitive_intel(payload: dict) -> dict:
    world = load_world()
    return envelope(
        "competitive_intel",
        {"matrix": world["competitors"], "northlamp_offer": world["northlamp_offer"]},
        ["Five competitor profiles in fixture"],
        [],
        [],
        focus_areas=_focus("Broaden geo coverage to match top competitors", "Gridwatt"),
    )


def financial_analyst(payload: dict) -> dict:
    commentary = load_world()["commentary"]
    return envelope(
        "financial_analyst",
        {
            "unusual": f"Northlamp: {commentary['Northlamp']}",
            "memo": "Q3 dip appears inventory and freight driven; monitor cash conversion.",
        },
        ["Q3 Northlamp FCF turned negative"],
        ["Recovery timing depends on restock execution"],
        [],
        focus_areas=_focus("Tighten cash and inventory planning cadence", "Lumenoak"),
    )


def spreadsheet_intel(payload: dict) -> dict:
    rows = load_world()["sales_rows"]
    return envelope(
        "spreadsheet_intel",
        {"anomalies": [r for r in rows if r["units"] < 50], "recommendation": "prioritize Mini restock"},
        ["Lamp-Mini unit collapse starts in May"],
        [],
        [],
        focus_areas=_focus("Introduce stockout forecasting by region", "Pinevolt"),
    )


def document_deck(payload: dict) -> dict:
    return envelope(
        "document_deck",
        {"slides": ["Executive summary", "Risk matrix", "90-day action plan"]},
        ["Deck scaffold built from operating fixture"],
        [],
        [],
        focus_areas=_focus("Automate role-specific narrative variants", "Harbor Beam"),
    )


def research_agent(payload: dict) -> dict:
    sources = load_world()["research_sources"]
    verified = [s for s in sources if s["verified"]]
    assumptions = [s["claim"] for s in sources if not s["verified"]]
    return envelope(
        "research_agent",
        {"verified_claims": verified},
        [s["claim"] for s in verified],
        assumptions,
        [],
        focus_areas=_focus("Increase source verification coverage before synthesis", "Lumenoak"),
    )


def legal_review(payload: dict) -> dict:
    contracts = load_world()["contracts"]
    flagged = [c["id"] for c in contracts if c["liability_cap"] != "2_million"]
    return envelope(
        "legal_review",
        {"flagged_contracts": flagged},
        ["Two supplier agreements deviate from liability cap policy"],
        [],
        ["contract_sign"],
        focus_areas=_focus("Automate clause drift detection against policy baseline", "Gridwatt"),
    )


def ecommerce_ops(payload: dict) -> dict:
    orders = load_world()["orders"]
    return envelope(
        "ecommerce_ops",
        {"at_risk_orders": [o["id"] for o in orders if not o["paid"] or not o["shipped"]]},
        ["Unpaid and unshipped order detected"],
        [],
        ["refund"],
        focus_areas=_focus("Connect payment and fulfillment exceptions earlier", "Noxa Home"),
    )


def startup_os(payload: dict) -> dict:
    week = load_world()["ops_week"]
    return envelope(
        "startup_os",
        {"weekly_packet": week, "asks": ["Resolve Mini restock PO", "Unblock inventory sync job"]},
        ["Revenue is below target this week"],
        [],
        [],
        focus_areas=_focus("Operational rhythm with explicit owner follow-through", "Pinevolt"),
    )


def data_science(payload: dict) -> dict:
    dataset = load_world()["dataset"]
    outliers = [r for r in dataset if r["defect_ppm"] >= 350]
    return envelope(
        "data_science",
        {"outliers": outliers, "next_test": "temperature-control intervention on line A"},
        ["Defect spike aligns with temperature increase"],
        [],
        [],
        focus_areas=_focus("Codify anomaly alerts for process drift", "Gridwatt"),
    )


def engineering_cad(payload: dict) -> dict:
    spec = load_world()["cad_spec"]
    return envelope(
        "engineering_cad",
        {"part": spec["part"], "checklist": ["socket clearance", "material tolerance review"]},
        ["M4 socket clearance constraint is explicit"],
        [],
        [],
        focus_areas=_focus("Automate constraint validation before handoff", "Lumenoak"),
    )


def it_ops(payload: dict) -> dict:
    incident = load_world()["it_incident"]
    return envelope(
        "it_ops",
        {"host": incident["host"], "diagnosis": "Session store connectivity failure"},
        ["Logs show redis connection refused"],
        [],
        ["infra_change"],
        focus_areas=_focus("Add automated rollback path for session-store faults", "Harbor Beam"),
    )


def marketing_ops(payload: dict) -> dict:
    campaigns = load_world()["campaigns"]
    return envelope(
        "marketing_ops",
        {"action": "Pause spend on stockout SKUs", "campaigns": campaigns},
        ["ROAS and CVR declined week-over-week"],
        [],
        [],
        focus_areas=_focus("Spend governance tied to inventory availability", "Noxa Home"),
    )


def healthcare_admin(payload: dict) -> dict:
    batch = load_world()["healthcare_admin"]
    return envelope(
        "healthcare_admin",
        {"batch_id": batch["batch_id"], "ready_records": [r for r in batch["records"] if r["status"] == "ready"]},
        ["Administrative records contain no PHI fields in fixture"],
        [],
        [],
        blocked=["clinical_decision"],
        focus_areas=_focus("Keep healthcare workflows administrative-only by default", "Harbor Beam"),
    )


def multi_agent(payload: dict) -> dict:
    return envelope(
        "multi_agent",
        {"plan": ["support_resolver", "financial_analyst", "marketing_ops"], "goal": payload.get("goal", "")},
        ["Route work to specialist engines and aggregate outputs"],
        [],
        [],
        focus_areas=_focus("Improve specialist routing confidence by task intent", "Lumenoak"),
    )


ENGINES = {
    "computer_agent": computer_agent,
    "coding_agent": coding_agent,
    "website_qa": website_qa,
    "support_resolver": support_resolver,
    "sales_crm": sales_crm,
    "competitive_intel": competitive_intel,
    "financial_analyst": financial_analyst,
    "spreadsheet_intel": spreadsheet_intel,
    "document_deck": document_deck,
    "research_agent": research_agent,
    "legal_review": legal_review,
    "ecommerce_ops": ecommerce_ops,
    "startup_os": startup_os,
    "data_science": data_science,
    "engineering_cad": engineering_cad,
    "it_ops": it_ops,
    "marketing_ops": marketing_ops,
    "healthcare_admin": healthcare_admin,
    "multi_agent": multi_agent,
}

if set(ENGINES) != set(CASES):
    missing = sorted(set(CASES) - set(ENGINES))
    extra = sorted(set(ENGINES) - set(CASES))
    raise RuntimeError(f"Engine registry mismatch. missing={missing}, extra={extra}")
