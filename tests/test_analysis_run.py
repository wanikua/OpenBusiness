import pytest

from openbusiness.analysis_run import AnalysisRunRequest, prepare_analysis_run


def test_prepare_analysis_run_resolves_profiles_language_and_state(tmp_path) -> None:
    prepared = prepare_analysis_run(
        AnalysisRunRequest(
            company="Example AI",
            output_dir=tmp_path,
            output_language="en",
            ui_language="en",
        )
    )

    assert prepared.domain == "exampleai.com"
    assert prepared.output_language == "en"
    assert prepared.ui_language == "en"
    assert prepared.analysis_pack.id == "general"
    assert prepared.report_template.id == "standard"
    assert prepared.initial_state["evidence_pack"] == ""
    assert prepared.initial_state["final_report"] == ""


def test_prepare_analysis_run_rejects_unknown_depth(tmp_path) -> None:
    with pytest.raises(ValueError, match="Unsupported analysis depth"):
        prepare_analysis_run(
            AnalysisRunRequest(
                company="Example",
                output_dir=tmp_path,
                output_language="en",
                ui_language="en",
                analysis_depth="shallow",
            )
        )
