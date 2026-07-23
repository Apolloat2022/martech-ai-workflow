# 0002. Decline to automate claims sign-off itself

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D2](../02-bottleneck-register.md)'s bottleneck register (B-10) scores the claims review handoffs (H4, H7) High-cost and clearly automatable-looking: unsubstantiated-claim detection is pattern-matchable, and an LLM can flag candidate issues with reasonable precision. The question is whether the model should also be allowed to *clear* an asset — auto-approve it when confidence is high — rather than only flag issues for a human.

## Decision Drivers

- Claims substantiation is a regulated judgment call with legal accountability attached to a specific reviewer, not a classification task with an acceptable error rate.
- [D10](../10-governance.md)'s EU AI Act mapping keeps UC-1/UC-2 at limited-risk specifically *because* a human remains in the loop for every sign-off — removing that would change the legal classification, not just the internal risk posture.

## Considered Options

- Human-only sign-off; the model only flags candidate issues for review (chosen)
- LLM auto-approval above a confidence threshold, with human review only below it
- LLM auto-approval with a random-sample human audit (no per-item human gate)

## Decision Outcome

Chosen option: human-only sign-off, because the exposure created by a wrong auto-approval — an unsubstantiated claim shipping externally — is not one any achievable model-quality bar removes. The risk is about *who is accountable*, not about accuracy. A confidence-threshold auto-approval scheme would eventually approve a wrong claim confidently, and "the model was 97% confident" is not a defensible position in a regulatory review. This is the anchor decision behind [D2](../02-bottleneck-register.md)'s B-10 "None" automation-candidacy row and [D7](../07-nfr-budgets.md)'s fail-closed policy-engine rule.

### Consequences

- Good, because the platform's risk profile is defensible to Legal & Compliance without qualification — no scenario exists where the AI layer alone is responsible for a claims decision.
- Bad, because the cycle-time benefit of automation is capped at "catch issues earlier" (moving rework upstream) rather than "remove the review step" — the queue depth behind B-08's staffing constraint is not something this decision can shrink.

## Links

- [D2 — Bottleneck & Redundancy Register](../02-bottleneck-register.md), row B-10
- [D7 — Non-Functional Requirements](../07-nfr-budgets.md), UC-1 degradation ladder
- [D10 — AI Governance Framework](../10-governance.md), Tier 1 HITL policy and EU AI Act mapping
