"""The policy engine - the single governance rule this slice enforces
end-to-end: unsubstantiated-claim detection routes to human review
(D2 B-10, D10 Tier 1 HITL policy, ADR 0002). This is the most important
module in the slice; everything else exists to feed it correctly.
"""
from __future__ import annotations


def _is_substantiated(phrase: str, context_chunks: list[str]) -> bool:
    """A claim is substantiated only if a retrieved claims-spec document
    explicitly marks it CLAIM-OK for the product in question (see
    corpus/claims_specs/*.md). Absence of any signal - including a document
    that only lists CLAIM-BLOCKED entries - defaults to unsubstantiated:
    the safe default, matching D2 B-10's philosophy of flagging when in
    doubt."""
    phrase_lower = phrase.lower()
    marker = f"claim-ok: {phrase_lower}"
    return any(marker in chunk.lower() for chunk in context_chunks)


def check(candidate_claims: list[str], retrieved_context: list[str]) -> tuple[str, list[str]]:
    if not candidate_claims:
        return "clear", ["no claim patterns requiring substantiation were found"]

    unsubstantiated = [c for c in candidate_claims if not _is_substantiated(c, retrieved_context)]
    if unsubstantiated:
        return "flagged_for_review", [
            f"'{phrase}' requires substantiation not found in retrieved context"
            for phrase in unsubstantiated
        ]
    return "clear", [
        f"'{phrase}' is substantiated by retrieved context" for phrase in candidate_claims
    ]


def safe_check(candidate_claims: list[str], retrieved_context: list[str]) -> tuple[str, list[str]]:
    """Fails closed, never open - ADR 0011. Any error in the policy check
    itself becomes flagged_for_review, never a silent clear."""
    try:
        return check(candidate_claims, retrieved_context)
    except Exception as exc:  # noqa: BLE001 - deliberately broad: fail closed on anything
        return "flagged_for_review", [
            f"policy engine error ({exc}); failing closed per ADR 0011 - not auto-cleared"
        ]
