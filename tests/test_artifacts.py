import json

from openbusiness.artifacts import write_run_artifacts


def test_write_run_artifacts_creates_report_manifest_and_sources(tmp_path) -> None:
    result = write_run_artifacts(
        output_dir=tmp_path,
        slug="example",
        final_state={
            "evidence_pack": "Pricing [VERIFIED:https://example.com/pricing]",
            "jtbd_report": "Customers [VERIFIED: https://example.com/customers ]",
            "final_report": "# Report\n\n[INFERRED]",
        },
        report="# Report\n\n[INFERRED]",
        warnings=[],
        company="Example",
        domain="example.com",
        ticker="",
        output_language="en",
        ui_language="en",
        analysis_depth="standard",
        analysis_pack="general",
        report_template="standard",
    )

    assert result.root_report_path.read_text(encoding="utf-8").startswith("# Report")
    assert (result.stages_dir / "01_evidence.md").exists()
    assert (result.stages_dir / "02_jtbd.md").exists()

    evidence = json.loads(result.evidence_path.read_text(encoding="utf-8"))
    assert evidence["verified_sources"] == [
        "https://example.com/pricing",
        "https://example.com/customers",
    ]

    run_meta = json.loads(result.run_meta_path.read_text(encoding="utf-8"))
    assert run_meta["paths"]["root_report"] == str(result.root_report_path)
    assert run_meta["evidence_label_policy"]["missing"].startswith("[MISSING]")
