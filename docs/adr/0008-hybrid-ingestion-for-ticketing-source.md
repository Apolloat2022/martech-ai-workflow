# 0008. Use hybrid webhook-plus-reconciliation ingestion for the ticketing source

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

S7 (the ticketing/workflow system) supplies brief content to the retrieval index. [D3](../03-data-landscape.md) flags that its webhooks exist but are used inconsistently — an unreliable event source. [D5](../05-data-pipelines.md) needed an ingestion mode that doesn't silently drop briefs while also not accepting an hour of latency on every single one.

## Decision Drivers

- A pure webhook subscription inherits the source's own reliability problem, and a silently dropped brief is worse than a late one — it means a brief never enters the retrieval corpus at all, with no error surfaced anywhere.
- A pure batch poll is simple and safe but adds up to an hour of latency to every brief, even the vast majority the webhook would have delivered correctly.

## Considered Options

- Webhook-only ingestion, matching S1/S2's event-driven pattern
- Batch-only ingestion (hourly poll), avoiding any dependency on webhook reliability
- Hybrid: webhook-first, with an hourly reconciliation poll as a fallback (chosen)

## Decision Outcome

Chosen option: hybrid ingestion. This accepts the batch poll's bounded, known latency (at most 60 minutes) as the worst case, rather than accepting the webhook's unbounded, silent drop risk as the normal case. The limiting factor here is the source's own reliability, not a preference between ingestion patterns — S1 and S2 get webhook-only ingestion in the same document because their webhooks are actually trustworthy; S7 doesn't get the same treatment because its webhook isn't.

### Consequences

- Good, because a dropped webhook for S7 is now a worst-case 60-minute delay, not a silent, undetected gap in the retrieval corpus.
- Bad, because the ingestion workers now run two code paths for this one source (event handler plus reconciliation job) instead of one, and the reconciliation job's own dedup logic (has this brief already been ingested via webhook?) is additional complexity the event-driven sources don't carry.

## Links

- [D3 — Data Landscape Assessment](../03-data-landscape.md), S7
- [D5 — Data Pipeline & Contract Design](../05-data-pipelines.md), ingestion mode table
