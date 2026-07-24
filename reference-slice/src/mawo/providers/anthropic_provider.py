"""Real model-provider adapter - opt-in via ANTHROPIC_API_KEY. Not exercised
by default; the mock provider is what this slice runs against with zero
API keys (see PROJECT_PLAN.md open question 2). Present and documented so
the model-abstraction interface is proven against a second implementation,
not just described.
"""
from __future__ import annotations

from ..policy.claims import find_candidate_claims
from .base import Provider, ProviderOutput


class AnthropicProvider(Provider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5") -> None:
        import anthropic

        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(
        self, use_case: str, input_data: dict, retrieved_context: list[str]
    ) -> ProviderOutput:
        prompt = self._build_prompt(use_case, input_data, retrieved_context)
        response = self._client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        narrative = text if use_case == "performance_readout_synthesis" else None
        return ProviderOutput(
            candidate_claims=find_candidate_claims(text),
            narrative=narrative,
            model=self.model,
            model_version=response.model,
        )

    def _build_prompt(
        self, use_case: str, input_data: dict, retrieved_context: list[str]
    ) -> str:
        context_block = "\n\n".join(retrieved_context)
        if use_case == "claims_brand_prescreen":
            return (
                "You are checking creative copy against brand and claims "
                f"guidelines.\n\nContext:\n{context_block}\n\n"
                f"Creative:\n{input_data['creative_text']}\n\n"
                "List any claims that need substantiation."
            )
        if use_case == "localization_claims_check":
            return (
                "You are checking localized copy for claims consistency.\n\n"
                f"Context:\n{context_block}\n\nSource:\n{input_data['source_text']}\n\n"
                f"Localized ({input_data['market_code']}):\n{input_data['localized_text']}\n\n"
                "Flag any claims-bearing phrases or drift from the source."
            )
        return f"Write a short, factual performance readout narrative from this data:\n{input_data}"
