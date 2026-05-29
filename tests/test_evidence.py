import json

from openbusiness.evidence import error_result, missing_result, source_tag, verified_result


def test_evidence_result_shapes() -> None:
    missing = json.loads(missing_result("tool", "missing key", "fallback", results=[]))
    error = json.loads(error_result("tool", "boom", url="https://example.com"))
    verified = json.loads(verified_result("tool", source_tag=source_tag("https://example.com")))

    assert missing["status"] == "missing"
    assert missing["fallback_action"] == "fallback"
    assert error["status"] == "error"
    assert verified["source_tag"] == "[VERIFIED:https://example.com]"
