from mawo.policy.engine import check, safe_check
from mawo.policy.claims import find_candidate_claims

SUBSTANTIATED_CONTEXT = """
Claim status for this product:
- CLAIM-OK: clinically tested (supported by MRG-STUDY-2025-014)
- CLAIM-BLOCKED: clinically proven
"""

UNSUBSTANTIATED_CONTEXT = """
Claim status for this product:
- CLAIM-BLOCKED: clinically proven
- CLAIM-BLOCKED: clinically tested
"""


def test_no_candidate_claims_is_clear():
    status, reasons = check([], [SUBSTANTIATED_CONTEXT])
    assert status == "clear"


def test_substantiated_claim_is_clear():
    status, reasons = check(["clinically tested"], [SUBSTANTIATED_CONTEXT])
    assert status == "clear"
    assert "substantiated" in reasons[0]


def test_unsubstantiated_claim_is_flagged():
    status, reasons = check(["clinically proven"], [SUBSTANTIATED_CONTEXT])
    assert status == "flagged_for_review"


def test_claim_with_no_context_at_all_is_flagged():
    status, reasons = check(["clinically proven"], [UNSUBSTANTIATED_CONTEXT])
    assert status == "flagged_for_review"


def test_safe_check_fails_closed_on_error():
    status, reasons = safe_check(["x"], None)  # None breaks the `in` check -> exception
    assert status == "flagged_for_review"
    assert "ADR 0011" in reasons[0]


def test_find_candidate_claims_is_case_insensitive():
    assert "guaranteed" in find_candidate_claims("This is GUARANTEED to work.")
