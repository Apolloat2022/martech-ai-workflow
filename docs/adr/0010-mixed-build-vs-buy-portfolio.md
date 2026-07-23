# 0010. Adopt a mixed build-vs-buy portfolio rather than a uniform strategy

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D8](../08-vendor-evaluation.md) evaluated Build against two vendor archetypes for each of UC-1, UC-2, and UC-3 using one fixed weighted rubric. A uniform strategy — build everything, or buy everything — is organizationally simpler than a mixed one: one contract negotiation or one engineering commitment, not both. The question is whether that simplicity is worth what it costs.

## Decision Drivers

- The same rubric, applied honestly, scored the three use cases differently — forcing a uniform answer would mean overriding at least one use case's actual score to preserve organizational simplicity.
- [D8](../08-vendor-evaluation.md)'s TCO model shows a uniform strategy is not even reliably cheaper: all-buy wins at pilot scale, but loses badly at post-expansion scale, and all-build's advantage is narrow at current scope.

## Considered Options

- Mixed portfolio: build UC-1 and UC-3, buy UC-2 (chosen)
- Uniform build: build all three in-house
- Uniform buy: buy all three from a vendor

## Decision Outcome

Chosen option: mixed portfolio, because UC-2's specific requirement — accurate, current, multi-market legal claims rules maintained indefinitely — is a specialized capability a vendor is structurally better positioned to carry than MRG's own small team, while UC-1 and UC-3 both score highest on Build for reasons specific to their own risk and cost profiles ([D8](../08-vendor-evaluation.md)'s weighted matrices). Forcing uniformity here would mean choosing organizational tidiness over the rubric's actual output — exactly the "matrix that always says build [or buy] is not an evaluation" failure this repo's quality bar names explicitly.

### Consequences

- Good, because each use case's sourcing strategy tracks what that use case specifically needs, not an org-wide policy that happens to fit some use cases by accident.
- Bad, because MRG now carries two vendor-management relationships worth of overhead instead of one uniform posture (a single vendor contract, or none) — one contract to manage (Vendor A for UC-2) plus in-house ownership for the other two, rather than a single simpler arrangement.

## Links

- [D8 — Vendor Evaluation & Build-vs-Buy](../08-vendor-evaluation.md)
