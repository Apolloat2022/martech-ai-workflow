# Non-Functional Requirements

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Platform engineering, SRE, solution architects.

All numbers below are `[illustrative]` — the latency harness in `reference-slice/bench/latency_harness.py` (Step 6, D12) produces `[measured]` numbers to compare against them. If Phase 2 is cut, this document ships with `[illustrative]` figures only, per [PROJECT_PLAN.md](../PROJECT_PLAN.md) section 0. Stage names in the decomposition tables match `TraceInfo.stage_timings_ms` in [D6](06-interface-spec.md)'s OpenAPI spec — the same six stages are what the reference slice's trace output actually reports.

## UC-1 — Claims & Brand Pre-Screen Assistant

Interactive: an agency creative or brand reviewer is waiting on this at their screen.

### Latency budget

*All figures `[illustrative]` until Step 6 produces `[measured]` numbers.*

| Stage | p50 | p95 | p99 |
|---|---|---|---|
| network_in | 20ms | 50ms | 80ms |
| retrieval | 150ms | 350ms | 600ms |
| rerank | 80ms | 200ms | 350ms |
| inference | 1,800ms | 3,500ms | 5,500ms |
| policy_check | 30ms | 80ms | 150ms |
| network_out | 20ms | 50ms | 80ms |
| **Stage sum** | **2,100ms** | **4,230ms** | **6,760ms** |
| **Budget (with ~15–20% headroom)** | **2.5s** | **5s** | **8s** |

Headroom over the raw stage sum covers queueing, GC pauses, and cold-start variance — the budget is not just the sum, deliberately.

- **Throughput `[illustrative]`:** 30 requests/minute sustained, bursting to 80/minute during pre-launch weeks.
- **Availability `[illustrative]`:** 99.5% monthly — capped at the DAM/CMS source chain's own published availability (see D5); error budget ≈ 3.6 hours/month.
- **Resilience posture:** stateless gateway, horizontally scalable on Fargate; retrieval index multi-AZ; one retry with jitter on the model-provider call (not more — a second retry under provider degradation amplifies load instead of relieving it); circuit breaker on the provider integration.

### Degradation ladder

1. Rerank fails → skip it, serve raw retrieval ranking. Quality degrades; service continues.
2. Retrieval index unavailable → fall back to keyword search over a cached snapshot. Relevance degrades; service continues.
3. Primary model provider unavailable → fail over to the mock/deterministic provider, output flagged `reduced_confidence`, **still always routes to human review** — never silently auto-clears on a degraded model.
4. Policy engine unavailable → **fail closed**: every request becomes `flagged_for_review`, none auto-clear. This is a hard rule, not a tunable — see D2's B-10 and D6's `policy_engine_error` (non-retriable by design).
5. Gateway itself unavailable → callers fall back to the pre-existing manual review workflow (the ticketing-based process this platform sits alongside). The AI layer is additive; its outage is not a business-process outage.

## UC-2 — Localization Claims Consistency Checker

Batch-tolerant: runs as part of each market's localization step, not while a human waits at a screen.

### Latency budget

*All figures `[illustrative]` until Step 6 produces `[measured]` numbers.*

| Stage | p50 | p95 | p99 |
|---|---|---|---|
| network_in | 20ms | 50ms | 80ms |
| retrieval (source text + market claims taxonomy) | 200ms | 450ms | 800ms |
| rerank | 60ms | 150ms | 300ms |
| inference (back-translation consistency + claims-phrase flagging, one call) | 9,940ms | 29,850ms | 59,700ms |
| policy_check | 30ms | 80ms | 150ms |
| network_out | 20ms | 50ms | 80ms |
| **Stage sum** | **10,270ms** | **30,630ms** | **61,110ms** |
| **Budget (with headroom)** | **15s** | **45s** | **90s** |

Same six stages as UC-1's `TraceInfo.stage_timings_ms`. The back-translation check and the claims-phrase flagging happen inside one `inference` call rather than as a separate stage — that's why UC-2's `inference` line is disproportionately larger than UC-1's, not because the stage vocabulary changed.

- **Throughput `[illustrative]`:** ~5 requests/minute peak, across up to 4 markets per campaign.
- **Availability `[illustrative]`:** 99% monthly — a check that runs late can be requeued within the same localization cycle without the same business cost as a stalled UC-1 request.
- **Resilience posture:** same gateway infrastructure as UC-1; no dedicated resilience investment beyond that, because this use case's own latency tolerance already absorbs most transient failures via simple retry.

### Degradation ladder

If the checker is unavailable entirely, localization proceeds through the existing manual per-market legal review (H7 in D1) exactly as it does today. There is no degraded-AI fallback to design here — the fallback is simply "don't automate this occurrence," which is both the honest answer and the cheapest one to build.

## UC-3 — Performance Readout Synthesis

Asynchronous, batch: one run per reporting cycle, not a concurrent-request workload. Presented as a completion-time distribution across historical cycle runs, for consistency with UC-1/UC-2's format.

### Completion-time budget

*All figures `[illustrative]` until Step 6 produces `[measured]` numbers.*

| Stage | p50 | p95 | p99 |
|---|---|---|---|
| network_in | negligible | negligible | negligible |
| retrieval (aggregation query against the metrics store) | 30s | 90s | 180s |
| rerank | n/a — no chunked documents to rerank; this use case reads pre-aggregated rows, not retrieved passages | | |
| inference (narrative synthesis) | 60s | 180s | 360s |
| policy_check (the narrative itself is checked for new unsubstantiated claims before it ships) | 5s | 15s | 30s |
| network_out (includes final formatting) | negligible | negligible | negligible |
| **Stage sum** | **95s** | **285s** | **570s** |
| **Budget (with headroom)** | **5 min** | **15 min** | **30 min** |

Same six stages as UC-1 and UC-2's `TraceInfo.stage_timings_ms`, not a different shape for a different use case. `rerank` is genuinely inapplicable here — it stays in the vocabulary as an explicit `n/a`, not a silently dropped row, and `policy_check` is not skipped just because the input data is already de-identified: a synthesis narrative can still assert a claim about campaign performance that isn't substantiated by the numbers behind it, and D4's Policy Engine runs on every response regardless of use case.

- **Throughput `[illustrative]`:** one run per reporting cycle (weekly) — not a concurrent-request workload, so a per-minute figure would misrepresent it rather than describe it.
- **Availability `[illustrative]`:** 98% monthly — the lowest of the three, deliberately: a failed run can be regenerated the next day with no cycle-critical dependency on it landing at a specific hour.
- **Resilience posture:** single scheduled job, no standing capacity held for it between runs.

### Degradation ladder

If narrative synthesis fails, the readout ships as the raw aggregated metrics table without the AI-generated narrative wrapper. The numbers — which are the part of the readout that actually matters — are unaffected by a model-provider outage; only the prose summary is missing, and it's clearly marked as such.

## Cross-use-case principle

Two rules hold across all three: the **policy engine fails closed, never open** (a governance check that silently degrades into auto-approval is worse than no check at all), and **the AI layer degrades toward the process that existed before it**, never toward a new failure mode nobody had to plan for previously. Every degradation ladder above ends at a state D1's process already knew how to operate in.

## What this changes

These budgets are what the reference slice's latency harness (D12, Step 6) is measured against. A `[measured]` number that beats its budget is good news to report as-is; a `[measured]` number that misses its budget gets a variance note explaining the gap, not a quiet edit to the target — see PROJECT_PLAN.md Step 6. The stage decomposition also fixes what D6's `TraceInfo` must report per request: any stage added to the real implementation that isn't one of these six names is a spec change to this document first, not an implementation detail.
