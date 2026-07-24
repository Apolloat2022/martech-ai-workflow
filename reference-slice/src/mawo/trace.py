"""Stage timer matching the six canonical stages in D6's
TraceInfo.stage_timings_ms and D7's budget tables: network_in, retrieval,
rerank, inference, policy_check, network_out.
"""
from __future__ import annotations

import time
from contextlib import contextmanager


class StageTimer:
    def __init__(self) -> None:
        self.timings_ms: dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.timings_ms[name] = (time.perf_counter() - start) * 1000

    def mark_na(self, name: str) -> None:
        """Explicit n/a, recorded as 0ms rather than omitted - see D7's
        UC-3 rerank row: a skipped stage is still named, not silently
        dropped."""
        self.timings_ms[name] = 0.0
