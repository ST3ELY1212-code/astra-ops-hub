from astra_ops.engines import ENGINES
from astra_ops.orchestrator import monitor_snapshot, run_all, run_case

def test_all_engines_return_envelope():
    for case_id, fn in ENGINES.items():
        result = fn({})
        assert result["case_id"] == case_id
        assert result["status"] in {"completed", "needs_approval", "blocked"}
        assert "artifact" in result
        assert isinstance(result["evidence"], list)
        assert isinstance(result["assumptions"], list)
        assert result["focus_areas"]

def test_support_does_not_auto_send():
    r = run_case("support_resolver", remember_run=False)
    assert "email_send" in r["approval_required"]
    assert r["status"] == "needs_approval"

def test_healthcare_blocks_clinical():
    r = run_case("healthcare_admin", remember_run=False)
    assert "clinical_decision" in r["blocked"]

def test_coding_emits_patch_and_test():
    r = run_case("coding_agent", remember_run=False)
    assert "persist_session" in r["artifact"]["patch"]
    assert "test_redis_down" in r["artifact"]["regression_test"]

def test_finance_flags_northlamp():
    r = run_case("financial_analyst", remember_run=False)
    assert "Northlamp" in r["artifact"]["unusual"]

def test_monitor_and_all():
    snap = monitor_snapshot()
    assert snap["healthy"]
    results = run_all(remember_run=False)
    assert len(results) == 19
