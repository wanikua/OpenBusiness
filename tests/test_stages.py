from openbusiness.stages import initial_stage_state, stage_artifacts, stage_labels, stage_outputs


def test_stage_catalog_drives_state_labels_and_artifacts() -> None:
    state = initial_stage_state()
    artifacts = stage_artifacts()
    labels = stage_labels("en")

    assert state["evidence_pack"] == ""
    assert artifacts["final_report"] == "09_final.md"
    assert labels["finalizer"].endswith("Report Finalizer")


def test_stage_outputs_returns_only_populated_outputs() -> None:
    outputs = list(stage_outputs({"evidence_pack": "Evidence", "final_report": ""}))

    assert outputs == [("evidence_pack", "01_evidence.md", "Evidence")]
