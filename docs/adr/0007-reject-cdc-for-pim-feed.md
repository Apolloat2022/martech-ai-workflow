# 0007. Reject CDC for the PIM feed; use daily batch

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D5](../05-data-pipelines.md) needed an ingestion mode for S5 (PIM), which supplies claims-relevant product specs to the retrieval index. Change data capture (CDC) is the more "modern" default for keeping a downstream store fresh, and was the first option considered for every source in the pipeline design, not just this one.

## Decision Drivers

- PIM's own source data only refreshes on a daily batch cadence, per [D3](../03-data-landscape.md).
- CDC infrastructure has a real, ongoing operational cost (connector maintenance, replication lag monitoring) that has to be justified by an actual freshness need.

## Considered Options

- Real-time CDC pipeline from PIM into the ingestion workers
- Daily batch ingestion, matching PIM's own refresh cadence (chosen)

## Decision Outcome

Chosen option: daily batch. CDC would chase a target that only moves once a day — the infrastructure buys zero freshness improvement, because the data it would be capturing changes doesn't change any faster than a nightly batch already reflects. This is the clearest instance in [D5](../05-data-pipelines.md) of matching pipeline sophistication to source behavior rather than to what's technically fashionable: CDC is the right answer for S1 and S2, which are genuinely event-driven at the source, and the wrong answer here for the same reason it's right there.

### Consequences

- Good, because the ingestion layer avoids maintaining CDC infrastructure (and the on-call burden that comes with it) for a source that cannot benefit from it.
- Bad, because if PIM's own refresh cadence ever changes to something faster (e.g. real-time attribute updates for a future use case), this decision needs revisiting — it is not evergreen, it is conditional on PIM's current behavior.

## Links

- [D3 — Data Landscape Assessment](../03-data-landscape.md), S5
- [D5 — Data Pipeline & Contract Design](../05-data-pipelines.md), ingestion mode table
