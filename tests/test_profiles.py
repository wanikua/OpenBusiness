import pytest

from openbusiness.profiles import ProfileRegistry


def test_profile_registry_loads_builtin_profiles() -> None:
    registry = ProfileRegistry()

    pack_ids = {pack.id for pack in registry.list_analysis_packs()}
    template_ids = {template.id for template in registry.list_report_templates()}

    assert "general" in pack_ids
    assert "standard" in template_ids


def test_profile_registry_rejects_invalid_pack(tmp_path) -> None:
    pack_file = tmp_path / "bad.toml"
    pack_file.write_text(
        'id = "bad"\nname = "Bad"\ndescription = "Missing focus lists."\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="evidence_focus"):
        ProfileRegistry().load_analysis_pack(file_path=str(pack_file))


def test_profile_registry_rejects_empty_template_body(tmp_path) -> None:
    template_file = tmp_path / "empty.md"
    template_file.write_text(
        '+++\nid = "empty"\nname = "Empty"\ndescription = "No body."\n+++\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="template body"):
        ProfileRegistry().load_report_template(file_path=str(template_file))


def test_profile_registry_reports_missing_custom_file(tmp_path) -> None:
    missing_file = tmp_path / "missing.toml"

    with pytest.raises(ValueError, match="Profile file not found"):
        ProfileRegistry().load_analysis_pack(file_path=str(missing_file))
