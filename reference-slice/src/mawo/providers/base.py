from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderOutput:
    candidate_claims: list[str]
    model: str
    model_version: str
    narrative: str | None = None


class Provider(ABC):
    @abstractmethod
    def generate(
        self, use_case: str, input_data: dict, retrieved_context: list[str]
    ) -> ProviderOutput: ...
