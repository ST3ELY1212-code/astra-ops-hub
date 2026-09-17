"""Shared policy: least privilege, evidence vs assumption, approval gates."""

from __future__ import annotations

WRITE_ACTIONS = {
    "crm_write",
    "refund",
    "email_send",
    "infra_change",
    "contract_sign",
    "clinical_decision",
    "payment_capture",
    "production_deploy",
    "phi_export",
}

BLOCKED_ALWAYS = {"clinical_decision", "unrestricted_root"}


def classify_claim(text: str, sourced: bool) -> str:
    return "evidence" if sourced else "assumption"


def gate(action: str, approved: bool = False) -> dict:
    if action in BLOCKED_ALWAYS:
        return {"allowed": False, "status": "blocked", "reason": f"{action} is never autonomous"}
    if action in WRITE_ACTIONS and not approved:
        return {"allowed": False, "status": "needs_approval", "reason": f"{action} requires a human"}
    return {"allowed": True, "status": "ok", "reason": "within policy"}


def envelope(
    case_id: str,
    artifact: dict,
    evidence: list,
    assumptions: list,
    approval_required: list,
    blocked: list | None = None,
    focus_areas: list | None = None,
    status: str | None = None,
) -> dict:
    if blocked:
        computed = "blocked"
    elif approval_required:
        computed = "needs_approval"
    else:
        computed = "completed"
    return {
        "case_id": case_id,
        "status": status or computed,
        "artifact": artifact,
        "evidence": evidence,
        "assumptions": assumptions,
        "approval_required": approval_required,
        "blocked": blocked or [],
        "focus_areas": focus_areas or [],
        "policy": {
            "writes_require_approval": True,
            "clinical_autonomy": False,
            "infra_unrestricted": False,
        },
    }
