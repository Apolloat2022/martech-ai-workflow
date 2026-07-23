# 0004. Decline to treat legal-review capacity as an AI problem

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D2](../02-bottleneck-register.md) (B-08) identifies that the claims-review queue stays deep regardless of how well-prepared assets arrive, because a small, centralized Legal & Compliance team reviews all four markets serially with no risk-based triage. An AI pre-screen (see [ADR 0002](0002-no-automated-claims-signoff.md)) reduces what reaches the queue, but the queue's depth is fundamentally a staffing and prioritization question. The question this ADR resolves: should this platform's roadmap include an "AI legal reviewer" to close the remaining gap, or should the gap be named as a staffing/process ask instead?

## Decision Drivers

- The pre-screen in [ADR 0002](0002-no-automated-claims-signoff.md) already captures the automatable share of this problem; what's left is capacity, not classification.
- Recommending more AI here would be recommending automation of a resourcing gap, which misrepresents the actual constraint to the people who could fix it (whoever owns Legal & Compliance staffing).

## Considered Options

- No further AI investment in this bottleneck; name it explicitly as a staffing/triage-policy gap outside this platform's scope (chosen)
- Build a second-tier AI reviewer authorized to clear low-risk items without human review, reducing queue volume directly
- Build an AI triage classifier that re-orders the queue by estimated risk, without granting any auto-clear authority

## Decision Outcome

Chosen option: no further AI investment, and name the gap explicitly as a staffing and triage-policy problem. A second-tier AI reviewer is a version of [ADR 0002](0002-no-automated-claims-signoff.md)'s rejected auto-approval path and fails for the same reason. A pure triage classifier (re-ordering, not clearing) was closer to viable, but was set aside for this repo's scope specifically — it's a real, buildable idea, just not the highest-value use of a third architecture slot alongside UC-1/UC-2/UC-3 (see [ADR 0005](0005-scope-exactly-three-ai-use-cases.md)), and it doesn't close B-08's actual constraint, which is headcount.

### Consequences

- Good, because this document is honest with whoever owns Legal & Compliance staffing: the remaining queue depth after the pre-screen ships is a resourcing conversation, not a pending engineering deliverable they're waiting on.
- Bad, because B-08's cycle-time cost is not closed by this repo's architecture at all — it is explicitly carried as an unsolved, out-of-scope constraint, which may read as an incomplete answer to a reviewer expecting every bottleneck to have a fix.

## Links

- [D2 — Bottleneck & Redundancy Register](../02-bottleneck-register.md), row B-08
- [ADR 0002 — No automated claims sign-off](0002-no-automated-claims-signoff.md)
