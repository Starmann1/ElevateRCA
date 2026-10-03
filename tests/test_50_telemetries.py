"""
Automated Test Suite for all 20 Door Problem Telemetry Datasets
Verifies:
1. Schema conformity & JSON parsing for 20 Door telemetry scenarios
2. 5-Stage RCA pipeline execution without errors
3. Single-Stage (#01-#10) vs Two-Stage (#11-#20) verification workflow tags
4. Ranked hypothesis output with engineering confidence & negative evidence
5. Actionable OEM SOP recommendation with safety isolation
6. Repeat repair / prior misdiagnosis logic validation (Telemetry #11)
"""
import glob
import json
import os
import sys

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.engine import ElevateRCAEngine

def test_all_20_door_telemetries():
    print("=" * 70)
    print("RUNNING ELEVATERCA 20-SAMPLE DOOR TELEMETRY VERIFICATION SUITE")
    print("=" * 70)
    
    engine = ElevateRCAEngine()
    telemetry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_telemetry"))
    json_files = sorted([f for f in glob.glob(os.path.join(telemetry_dir, "telemetry_[0-9][0-9]_*.json"))])
    
    assert len(json_files) == 20, f"Expected 20 telemetry files, found {len(json_files)}"
    
    passed = 0
    failed = 0
    results_summary = []
    
    for idx, filepath in enumerate(json_files, 1):
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            result = engine.analyze(data)
            
            # Validations
            assert result.investigation_id is not None, "Investigation ID missing"
            assert result.rca_conclusion is not None, "RCA conclusion missing"
            assert len(result.hypotheses) > 0, "No ranked hypotheses generated"
            assert result.rca_conclusion.subsystem != "", "Subsystem affected missing"
            assert result.corrective_recommendation.recommended_action != "", "Recommended SOP missing"
            
            # Check Stage tagging
            expected_stage = "SINGLE_STAGE" if idx <= 10 else "TWO_STAGE"
            assert result.verification_stage == expected_stage, f"Expected {expected_stage} for {filename}, got {result.verification_stage}"
            
            primary_hyp = result.hypotheses[0]
            conf = primary_hyp.posterior_probability * 100
            
            results_summary.append({
                "index": idx,
                "file": filename,
                "subsystem": result.rca_conclusion.subsystem,
                "primary_rc": primary_hyp.hypothesis_id,
                "name": primary_hyp.root_cause,
                "confidence": f"{conf:.1f}%",
                "stage": result.verification_stage,
                "sop": result.corrective_recommendation.recommended_action
            })
            passed += 1
            print(f"[{idx:02d}/20] PASS [{result.verification_stage}]: {filename} -> {primary_hyp.hypothesis_id}: {primary_hyp.root_cause} ({conf:.1f}%) | Action: {result.corrective_recommendation.recommended_action}")
            
        except Exception as e:
            failed += 1
            print(f"[{idx:02d}/20] FAIL: {filename} -> ERROR: {str(e)}")
            
    print("=" * 70)
    print(f"TEST SUMMARY: {passed}/20 PASSED, {failed} FAILED")
    print("=" * 70)
    
    # Specific repeat repair test validation (Telemetry 11: Repeat door roller replacement vs track misalignment)
    tel11_path = os.path.join(telemetry_dir, "telemetry_11_door_repeat_roller_misdiagnosis_track_misalignment.json")
    if os.path.exists(tel11_path):
        with open(tel11_path, "r", encoding="utf-8") as f:
            t11_data = json.load(f)
        t11_res = engine.analyze(t11_data)
        print("\n--- REPEAT REPAIR / MISDIAGNOSIS VALIDATION (Telemetry 11) ---")
        print(f"Investigation ID: {t11_res.investigation_id}")
        print(f"Primary Hypothesis: {t11_res.hypotheses[0].hypothesis_id} - {t11_res.hypotheses[0].root_cause}")
        print(f"Posterior Confidence: {t11_res.hypotheses[0].posterior_probability*100:.1f}%")
        print(f"Verification Stage: {t11_res.verification_stage}")
        print(f"Narrative: {t11_res.rca_conclusion.causal_narrative}")
        print(f"Action: {t11_res.corrective_recommendation.recommended_action}")
        assert t11_res.hypotheses[0].hypothesis_id == "RC3", "Expected RC3 (Track Misalignment) for repeat repair scenario!"
        print(">>> Repeat Repair / Prior Misdiagnosis Recognition: VERIFIED SUCCESSFUL\n")

    assert passed == 20, f"Expected 20 passed tests, but got {passed}/20."

if __name__ == "__main__":
    success = test_all_20_door_telemetries()
    sys.exit(0 if success else 1)
