"""Shared claim-pattern scan, used by both providers and the policy engine.

The phrase list mirrors corpus/brand_guidelines/prohibited_claims.md - claim
patterns MRG's brand guidelines flag as requiring substantiation before they
can ship.
"""
from __future__ import annotations

RISKY_CLAIM_PHRASES = [
    "clinically proven",
    "clinically tested",
    "guaranteed results",
    "guaranteed",
    "#1",
    "best-selling",
    "top-rated",
    "cures",
    "eliminates",
    "permanently removes",
    "chemical-free",
    "clean",
    "natural",
]


def find_candidate_claims(text: str) -> list[str]:
    lower = text.lower()
    return [phrase for phrase in RISKY_CLAIM_PHRASES if phrase in lower]
