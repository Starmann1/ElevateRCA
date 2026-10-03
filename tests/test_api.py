"""
Unit & Integration Tests for ElevateRCA FastAPI Backend
"""

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_api_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["safety_boundary"] == "READ_ONLY_ADVISORY"


def test_api_case_lifecycle_e2e():
    # 1. Create Case
    create_payload = {
        "asset_id": "ELEV-API-01",
        "subsystem": "Door",
        "symptoms": ["Door close timeout on floor 3"],
        "active_faults": ["E501 Door Close Timeout"],
        "configuration": {
            "model": "KONE MonoSpace DX",
            "egov": "A",
        },
    }
    res_create = client.post("/api/v1/cases", json=create_payload)
    assert res_create.status_code == 200
    case_data = res_create.json()
    case_id = case_data["case_id"]
    assert case_data["iteration"] == 1
    assert case_data["status"] == "RCA_PROPOSED"
    assert len(case_data["hypotheses"]) >= 2

    # 2. Get Case
    res_get = client.get(f"/api/v1/cases/{case_id}")
    assert res_get.status_code == 200
    assert res_get.json()["case_id"] == case_id

    # 3. Submit Technician Feedback (Negative evidence on roller + Positive on track)
    feedback_payload = {
        "feedback_text": "I inspected the roller: there is no visible wear and it rotates freely. The door becomes harder to move near fully closed."
    }
    res_fb = client.post(f"/api/v1/cases/{case_id}/technician-feedback", json=feedback_payload)
    assert res_fb.status_code == 200
    fb_data = res_fb.json()
    assert fb_data["iteration"] == 2
    assert fb_data["status"] == "RCA_REVISED"

    # Verify roller hypothesis was ruled out
    roller_hypo = next(h for h in fb_data["hypotheses"] if h["hypothesis_id"] == "HYP-DOOR-ROLLER")
    assert roller_hypo["state"] == "RULED_OUT"

    # 4. Record Diagnostic Confirmation Test (Confirming debris in track)
    test_payload = {
        "test_id": "TEST-TRACK-01",
        "outcome": "FAIL",
        "notes": "Bottom sill track full of construction grit",
    }
    res_test = client.post(f"/api/v1/cases/{case_id}/diagnostic-test", json=test_payload)
    assert res_test.status_code == 200
    test_data = res_test.json()
    assert test_data["iteration"] == 3
    assert test_data["status"] == "CORRECTIVE_ACTION"
    assert "CONFIRMED" in test_data["current_root_cause"]

    # 5. Submit Post-Repair Validation (Repaired & Passed)
    val_payload = {
        "fault_cleared": True,
        "cycles_passed": 5,
        "recurrence_observed": False,
        "notes": "Track cleaned and lubricated with silicone. 5 cycles completed without error.",
    }
    res_val = client.post(f"/api/v1/cases/{case_id}/post-repair-validation", json=val_payload)
    assert res_val.status_code == 200
    val_data = res_val.json()
    assert val_data["status"] == "CLOSED"

    # 6. Retrieve Final 21-Section Report
    res_rep = client.get(f"/api/v1/cases/{case_id}/report")
    assert res_rep.status_code == 200
    rep_markdown = res_rep.json()["report_markdown"]
    assert "1. INCIDENT SUMMARY" in rep_markdown
    assert "4. PRIMARY ROOT-CAUSE HYPOTHESIS" in rep_markdown
    assert "10. WHAT WOULD CHANGE THE DIAGNOSIS?" in rep_markdown
    assert "17. POST-REPAIR VALIDATION" in rep_markdown
    assert "21. CONFIDENCE / EVIDENCE STATUS" in rep_markdown
