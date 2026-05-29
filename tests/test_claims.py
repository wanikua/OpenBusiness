from openbusiness.claims import MISSING_LABEL, claim_label_policy, extract_verified_sources, verified_source_tag


def test_extract_verified_sources_deduplicates_in_order() -> None:
    sources = extract_verified_sources(
        "A [VERIFIED:https://example.com/a] B [VERIFIED:https://example.com/b]",
        "Again [VERIFIED:https://example.com/a] and spaced [VERIFIED: https://example.com/c ]",
    )

    assert sources == [
        "https://example.com/a",
        "https://example.com/b",
        "https://example.com/c",
    ]


def test_verified_source_tag_requires_url() -> None:
    assert verified_source_tag("https://example.com") == "[VERIFIED:https://example.com]"
    assert verified_source_tag("  ") == MISSING_LABEL


def test_claim_label_policy_is_stable_copy() -> None:
    policy = claim_label_policy()
    policy["verified"] = "mutated"

    assert claim_label_policy()["verified"].startswith("[VERIFIED:url]")
