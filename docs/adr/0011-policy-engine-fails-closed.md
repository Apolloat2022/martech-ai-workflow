# 0011. Fail closed, not open, on policy-engine unavailability

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D4](../04-target-architecture.md)'s Policy Engine runs on every gateway response, for every use case, before it's returned. [D7](../07-nfr-budgets.md) needed a degradation behavior for the case where the Policy Engine itself is unreachable — every other component in the gateway's degradation ladder (retrieval, rerank, the model provider) has a "degrade gracefully and keep serving" fallback. The question is whether the Policy Engine should get the same treatment.

## Decision Drivers

- The Policy Engine is the component that enforces [D2](../02-bottleneck-register.md) B-10 and [ADR 0002](0002-no-automated-claims-signoff.md) — its unavailability is not equivalent to a quality-degradation event like a reranker outage.
- Availability and governance correctness are in direct tension exactly at this one component, and only this one.

## Considered Options

- Fail open: if the Policy Engine is unreachable, return the model's output directly without a verdict, prioritizing availability (rejected)
- Fail closed: if the Policy Engine is unreachable, every request becomes `flagged_for_review`, prioritizing governance correctness over availability (chosen)
- Queue requests until the Policy Engine recovers, rather than either failing open or closed

## Decision Outcome

Chosen option: fail closed. A governance check that silently degrades into auto-approval during an outage is worse than no check at all, because it fails exactly when failure is least visible — nobody is watching more closely during a policy-engine outage than during normal operation, so a fail-open design converts an infrastructure incident into an undetected governance incident. Queuing (the third option) was rejected because it doesn't resolve the tension, it postpones it, and a queued claims-review request has the same cycle-time cost as the manual process this platform exists to shorten. This decision is reflected directly in [D6](../06-interface-spec.md)'s error taxonomy: `policy_engine_error` is the one non-retriable 5xx, specifically so a client can't retry its way toward an auto-clear.

### Consequences

- Good, because there is no failure mode in this architecture where an unreviewed claim can auto-publish — availability problems degrade toward more human review, never less.
- Bad, because a Policy Engine outage now has an amplifying effect on the human-review queue exactly when engineering attention is already consumed by the outage itself — the worst possible time for review volume to spike.

## Links

- [D2 — Bottleneck & Redundancy Register](../02-bottleneck-register.md), row B-10
- [D6 — Interface & Integration Spec](../06-interface-spec.md), error taxonomy
- [D7 — Non-Functional Requirements](../07-nfr-budgets.md), degradation ladders and "Cross-use-case principle"
- [ADR 0002 — No automated claims sign-off](0002-no-automated-claims-signoff.md)
