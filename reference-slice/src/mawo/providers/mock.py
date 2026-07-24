"""Deterministic, rule-based stand-in for a real model call. Runs with zero
API keys - this is the default provider, per PROJECT_PLAN.md open question 2.
"""
from __future__ import annotations

import hashlib

from ..policy.claims import find_candidate_claims
from .base import Provider, ProviderOutput


class MockProvider(Provider):
    model = "mock-deterministic"
    model_version = "1.0.0"

    def generate(
        self, use_case: str, input_data: dict, retrieved_context: list[str]
    ) -> ProviderOutput:
        if use_case == "claims_brand_prescreen":
            text = input_data["creative_text"]
            return ProviderOutput(
                candidate_claims=find_candidate_claims(text),
                model=self.model,
                model_version=self.model_version,
            )
        if use_case == "localization_claims_check":
            text = input_data["localized_text"]
            return ProviderOutput(
                candidate_claims=find_candidate_claims(text),
                model=self.model,
                model_version=self.model_version,
            )
        if use_case == "performance_readout_synthesis":
            narrative = self._synthesize_readout(input_data)
            return ProviderOutput(
                candidate_claims=find_candidate_claims(narrative),
                narrative=narrative,
                model=self.model,
                model_version=self.model_version,
            )
        raise ValueError(f"unsupported use_case: {use_case}")

    def _synthesize_readout(self, input_data: dict) -> str:
        """Deterministic pseudo-metrics standing in for the
        lifecycle-segment-feed contract's real aggregated data - wiring an
        actual metrics store is out of scope for an 800-line reference
        slice (see D5)."""
        lines = [f"Performance readout for cycle {input_data['cycle_id']}:"]
        for segment_id in input_data["segment_ids"]:
            seed = int(hashlib.sha256(segment_id.encode()).hexdigest(), 16)
            count = 50 + (seed % 450)
            rate = round(1 + (seed % 2000) / 100, 1)
            lines.append(
                f"- Segment {segment_id}: {count} reachable members, "
                f"{rate}% engagement rate this cycle."
            )
        return "\n".join(lines)
