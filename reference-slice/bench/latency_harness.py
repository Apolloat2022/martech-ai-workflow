"""Runs N synthetic invoke calls per use case against the mock provider (no
API keys required) and reports p50/p95/p99 per stage, to compare against
docs/07-nfr-budgets.md.

IMPORTANT: this measures the mock provider, which responds in
microseconds - it validates the pipeline's non-inference overhead
(retrieval, rerank, policy_check, network placeholders) against budget,
not real model-provider inference latency. See docs/07-nfr-budgets.md's
"Budget variance" note for what these numbers do and don't show.

Usage: python bench/latency_harness.py
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import os

os.environ["MAWO_DB_PATH"] = ":memory:"

from mawo import store  # noqa: E402
from mawo.gateway import build_indexes, run_invoke  # noqa: E402
from mawo.schemas import InvokeRequest, UseCase  # noqa: E402

N_RUNS = 200

REQUESTS = {
    UseCase.CLAIMS_BRAND_PRESCREEN: InvokeRequest(
        use_case=UseCase.CLAIMS_BRAND_PRESCREEN,
        submitted_by="bench-harness",
        input={
            "creative_text": "Our new serum is clinically tested and delivers guaranteed results.",
            "brief_id": "BENCH-001",
            "product_ids": ["GS-X1-30ML"],
        },
    ),
    UseCase.LOCALIZATION_CLAIMS_CHECK: InvokeRequest(
        use_case=UseCase.LOCALIZATION_CLAIMS_CHECK,
        submitted_by="bench-harness",
        input={
            "localized_text": "Notre serum est cliniquement teste et garanti.",
            "source_text": "Our serum is clinically tested and guaranteed.",
            "market_code": "EU",
            "brief_id": "BENCH-002",
        },
    ),
    UseCase.PERFORMANCE_READOUT_SYNTHESIS: InvokeRequest(
        use_case=UseCase.PERFORMANCE_READOUT_SYNTHESIS,
        submitted_by="bench-harness",
        input={"cycle_id": "BENCH-CYCLE-01", "segment_ids": ["seg-eu-01", "seg-us-02"]},
    ),
}

STAGES = ["network_in", "retrieval", "rerank", "inference", "policy_check", "network_out"]


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(int(len(ordered) * pct), len(ordered) - 1)
    return ordered[idx]


def run() -> dict:
    build_indexes()
    store.init_db()
    results: dict[str, dict[str, list[float]]] = {}
    for use_case, request in REQUESTS.items():
        stage_samples: dict[str, list[float]] = {stage: [] for stage in STAGES}
        for _ in range(N_RUNS):
            response = run_invoke(request)
            for stage in STAGES:
                stage_samples[stage].append(response.trace.stage_timings_ms.get(stage, 0.0))
        results[use_case.value] = stage_samples
    return results


def report(results: dict) -> None:
    for use_case, stage_samples in results.items():
        print(f"\n== {use_case} (n={N_RUNS}, mock provider) ==")
        print(f"{'stage':<14}{'p50 (ms)':>12}{'p95 (ms)':>12}{'p99 (ms)':>12}")
        total_p50 = total_p95 = total_p99 = 0.0
        for stage in STAGES:
            values = stage_samples[stage]
            p50, p95, p99 = (
                percentile(values, 0.50),
                percentile(values, 0.95),
                percentile(values, 0.99),
            )
            total_p50 += p50
            total_p95 += p95
            total_p99 += p99
            print(f"{stage:<14}{p50:>12.3f}{p95:>12.3f}{p99:>12.3f}")
        print(f"{'TOTAL':<14}{total_p50:>12.3f}{total_p95:>12.3f}{total_p99:>12.3f}")


if __name__ == "__main__":
    report(run())
