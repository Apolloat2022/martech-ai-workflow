# 0009. Target AWS, not Azure, for the deployment view

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

The JD this repo is written against lists Azure, AWS, and GCP as acceptable cloud platforms, and MRG is a fictional enterprise retailer of the kind that plausibly runs a Microsoft-centric stack. [D4](../04-target-architecture.md) needed one concrete cloud for its deployment view rather than a cloud-agnostic non-answer.

## Decision Drivers

- A deployment diagram that can't survive a follow-up question in an interview is worse than no deployment diagram.
- The author's actual depth is in AWS, not Azure.

## Considered Options

- Target AWS, with an Azure equivalence table to cover the "we're a Microsoft shop" case (chosen)
- Target Azure, to better match a stereotypical enterprise marketing stack
- Present both clouds in parallel, cloud-agnostically

## Decision Outcome

Chosen option: AWS with an Azure equivalence table. AWS is not architecturally superior for this workload — the [D4](../04-target-architecture.md) Azure equivalence table shows most components map cleanly. The deciding factor is defensibility under questioning, not technical merit: a deployment view built on unfamiliar ground reads as decoration the moment someone asks a follow-up question about it. Presenting both clouds in parallel (the third option) was rejected as the worst of both — it commits to neither and demonstrates depth in neither.

### Consequences

- Good, because the deployment view in [D4](../04-target-architecture.md) can be defended in detail, and the Azure equivalence table means a "we're a Microsoft shop" objection costs one paragraph, not a redesign.
- Bad, because the managed-inference row in that same table is a real, not cosmetic, portability gap — model catalogue differences between Bedrock and Azure OpenAI/AI Foundry are the actual switching cost or a future Azure migration, and this decision doesn't remove that cost, only names it honestly.

## Links

- [D4 — To-Be AI Architecture](../04-target-architecture.md), "Deployment view (AWS)" and Azure equivalence table
- [D8 — Vendor Evaluation & Build-vs-Buy](../08-vendor-evaluation.md), lock-in analysis (same argument, applied to a vendor rather than a cloud)
