# 0006. Exclude PII-flagged sources from the retrieval index; pre-aggregate instead

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

UC-3 (Performance Readout Synthesis) needs lifecycle and CDP data (S3, S4 — both PII-flagged per [D3](../03-data-landscape.md)) to generate its narrative. [D4](../04-target-architecture.md)'s retrieval index otherwise holds chunked, embedded content from S1/S2/S5/S7 and is queried directly by the model at inference time. The question is whether S3/S4 should be indexed the same way, with row-level records masked or redacted, or handled through a structurally different path.

## Decision Drivers

- Masking/redaction applied at query time is a policy control, not a structural one — a prompt-injection or retrieval-ranking bug could still surface an unmasked row.
- [D3](../03-data-landscape.md) flags consent state as the single highest-sensitivity field in the entire data landscape.

## Considered Options

- Index S3/S4 directly, with PII fields masked or redacted before embedding (rejected)
- Exclude S3/S4 from the retrieval index entirely; pre-aggregate into a separate metrics store with a data contract enforcing a minimum-count suppression floor (chosen)
- Index S3/S4 unmasked, relying on the policy engine to catch any PII in a response before it's returned

## Decision Outcome

Chosen option: exclude S3/S4 from the retrieval index entirely. Masking at embedding time is fragile — it depends on every future ingestion change correctly re-applying the mask, and a retrieval system's job is to surface relevant content, which is in tension with a masking step whose job is to suppress it. Pre-aggregation with a contractual suppression floor (see [D5](../05-data-pipelines.md)'s `lifecycle-segment-feed`) is a structural guarantee instead of a runtime one: there is no row-level record anywhere behind the metrics store for a bug to accidentally surface. Relying on the policy engine alone (the third option) was rejected because it makes the last line of defense the only line of defense — the same principle behind [D7](../07-nfr-budgets.md)'s fail-closed policy-engine rule applies here in reverse: don't design a system where a single control's failure is catastrophic when a structural exclusion is available instead.

### Consequences

- Good, because [D4](../04-target-architecture.md)'s trust-boundary diagram can state, as a structural fact rather than a policy promise, that no PII-flagged source ever enters the retrieval index.
- Bad, because UC-3 cannot answer questions requiring row-level granularity (e.g. "which specific customers" rather than "how many") — a real capability limitation, accepted deliberately rather than discovered later.

## Links

- [D3 — Data Landscape Assessment](../03-data-landscape.md), S3 and S4
- [D4 — To-Be AI Architecture](../04-target-architecture.md), trust-boundary diagram
- [D5 — Data Pipeline & Contract Design](../05-data-pipelines.md), `lifecycle-segment-feed` contract
