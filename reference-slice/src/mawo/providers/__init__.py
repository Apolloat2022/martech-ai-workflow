from __future__ import annotations

import os

from .base import Provider
from .mock import MockProvider


def get_provider() -> Provider:
    """Mock by default; real adapter opt-in via ANTHROPIC_API_KEY - see
    PROJECT_PLAN.md open question 2."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return MockProvider()
    from .anthropic_provider import AnthropicProvider

    return AnthropicProvider(api_key=api_key)
