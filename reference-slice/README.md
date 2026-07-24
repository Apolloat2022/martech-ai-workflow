# MAWO Reference Slice

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

A small, runnable proof that [D5](../docs/05-data-pipelines.md), [D6](../docs/06-interface-spec.md), [D7](../docs/07-nfr-budgets.md), and [D10](../docs/10-governance.md) describe something executable, not decoration. This is deliberately not a platform — see `PROJECT_PLAN.md`'s ~70/30 artifacts-to-code ratio and the hard constraints below.

## Quickstart

```bash
docker compose up
```

No API keys required — the gateway defaults to a deterministic mock provider. Once it's up:

```bash
curl http://localhost:8000/v1/health

curl -X POST http://localhost:8000/v1/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "claims_brand_prescreen",
    "submitted_by": "demo",
    "input": {
      "creative_text": "Hydra Boost Cream is clinically proven to guarantee results.",
      "brief_id": "DEMO-1",
      "product_ids": ["HBC-50ML"]
    }
  }'
```

That request should come back `"policy_verdict": {"status": "flagged_for_review", ...}` — Hydra Boost Cream has no substantiation on file for either phrase (see `corpus/claims_specs/hydra-boost-cream.md`). Swap the product and claim for Glow Serum X1's "clinically tested" and the same request comes back `"status": "clear"`, because that claim *is* substantiated (`corpus/claims_specs/glow-serum-x1.md`). That contrast — not just "the model runs" — is the actual thing this slice demonstrates: [D10](../docs/10-governance.md)'s one governance rule, enforced end-to-end, against real (if synthetic) data.

To opt into the real model-provider adapter instead of the mock: copy `.env.example` to `.env`, set `ANTHROPIC_API_KEY`, and re-run `docker compose up`.

## What's implemented, and what's cut

Implemented: `POST /v1/invoke` (all three use cases), `POST /v1/feedback`, `GET /v1/health`, the full pipeline (retrieval → rerank → provider call → policy check → trace), a mock provider and a real Anthropic adapter behind one interface, SQLite-backed trace and feedback persistence, and a latency harness.

**Cut, deliberately:** `POST /v1/stream` from [D6](../docs/06-interface-spec.md)'s OpenAPI spec is not implemented — streaming adds real complexity (SSE handling, partial-output framing) for no demonstrative value in a reference slice whose job is to prove the pipeline and the policy check are real, not to prove every documented endpoint exists. UC-3's metrics store is also not wired to a real aggregation pipeline; the mock provider generates deterministic pseudo-metrics from the segment IDs it's given, standing in for [D5](../docs/05-data-pipelines.md)'s `lifecycle-segment-feed` contract, since building a real metrics store is out of scope for an ~800-line slice and D5 already specifies what that contract looks like in full.

## Architecture

One service, per `PROJECT_PLAN.md`'s "no standalone vector store container" decision (see [ADR 0006](../docs/adr/0006-exclude-pii-sources-from-retrieval-index.md) for the related PII-exclusion reasoning). Retrieval is in-memory cosine similarity over deterministic bag-of-words vectors (`src/mawo/retrieval/`) — no embedding API, no vector database. Persistence is a single SQLite file (`src/mawo/store.py`) for trace and feedback records, mounted as a Docker volume so it survives container restarts.

The policy engine (`src/mawo/policy/engine.py`) is the module this whole slice exists to prove out: it enforces exactly the rule [D2](../docs/02-bottleneck-register.md) B-10 and [D10](../docs/10-governance.md)'s Tier 1 HITL policy describe — unsubstantiated-claim detection routes to human review — and it fails closed on any internal error, per [ADR 0011](../docs/adr/0011-policy-engine-fails-closed.md). That fail-closed behavior is implemented in code (`safe_check`), not just documented.

## Line budget

`src/mawo/` is ~650 lines — inside the plan's ~800-line guidance for the implementation. That guidance is read here as applying to the implementation specifically; `tests/` (~150 lines) and `bench/` (~90 lines) are kept lean but aren't squeezed to fit inside the same number, since discarding test coverage to hit a line-count target would be the wrong trade.

## Running tests and the latency harness

```bash
pip install -e ".[dev]"
pytest
python bench/latency_harness.py
```

The harness runs 200 requests per use case against the mock provider and reports p50/p95/p99 per stage. **Read [D7](../docs/07-nfr-budgets.md)'s "Step 6 measurement note" before interpreting the numbers** — the mock provider's "inference" stage is a string scan, not a model call, so the measured numbers are 3–4 orders of magnitude faster than budget for a reason that has nothing to do with the real system's expected performance. What the harness does validate honestly: the pipeline's non-inference overhead (retrieval, rerank, policy_check) is negligible against budget, which is the result you'd want regardless of which model provider eventually sits behind the `inference` stage.
