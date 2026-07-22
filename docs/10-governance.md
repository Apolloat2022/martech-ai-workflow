# AI Governance Framework

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Legal, risk, compliance, and marketing leadership.

This framework governs the three use cases in [D4](04-target-architecture.md) and is written to extend to any future marketing AI use case MRG proposes — the tiering and HITL rules below are a general test, not a description retrofitted to fit three examples.

## Risk tiering

| Tier | Test | Use cases |
|---|---|---|
| **Tier 1 — High** | Output touches regulated claims/legal substantiation, or could reach an external audience with brand or legal exposure if wrong | UC-1, UC-2 |
| **Tier 2 — Medium** | Output shapes an internal decision or artifact but doesn't itself reach an external audience and doesn't touch regulated claims | UC-3 |
| **Tier 3 — Low** | Internal tooling assistance where a human fully authors the final output; the AI never produces a standalone artifact | No current use case — described here for completeness, since a future proposal (e.g. a drafting-suggestion tool with no claims exposure) would need a tier to land in |

## HITL policy, per tier

| Tier | Who reviews | When | Accountable for |
|---|---|---|---|
| **1** | Brand reviewer (creative fit) and Legal & Compliance reviewer (claims substantiation) — matching [D1](01-current-state-process-map.md)'s existing review roles, not a new role invented for AI | Before any output can proceed past `flagged_for_review` — mandatory, non-bypassable, per [D2](02-bottleneck-register.md) B-10 and [D7](07-nfr-budgets.md)'s fail-closed policy-engine rule | The human reviewer is the accountable party of record for the sign-off decision itself. The AI output is advisory only — see D2 B-10, this is not a tunable position, it's the framework's foundation |
| **2** | Product Marketing Manager (the readout's owner) | Sampled audit against the policy-check verdict, not mandatory pre-publish sign-off on every run — the numbers underneath the narrative are already governed by the [D5](05-data-pipelines.md) contract; the narrative wrapper is what's being spot-checked | The PMM is accountable for what's published under their name, informed by the AI-flagged review sample and the policy check's own new-claim detection ([D7](07-nfr-budgets.md)) |
| **3** | The human author | Ongoing, inherent — a suggestion-only tool has no independent output to review | The human author, entirely — this tier exists precisely because there's no AI-authored artifact to assign separate accountability to |

## Mapping to NIST AI RMF

| NIST function | How this repo addresses it |
|---|---|
| **Govern** | This document, plus the accountable-owner assignments in the HITL table above and the vendor risk criteria below |
| **Map** | [D2](02-bottleneck-register.md)'s bottleneck register, [D3](03-data-landscape.md)'s data inventory, and [D4](04-target-architecture.md)'s trust boundaries — the risk surface is mapped before it's governed |
| **Measure** | [D7](07-nfr-budgets.md)'s NFR budgets and degradation ladders, plus the policy-verdict and reviewer-feedback loop ([D6](06-interface-spec.md)'s `/v1/feedback`) that measures whether Tier 1 sign-offs agree with or override the AI's flag over time |
| **Manage** | The degradation ladders ([D7](07-nfr-budgets.md)), the incident path below, and model/prompt change control below |

## Mapping to EU AI Act obligation classes

**Not legal advice — an illustrative classification for architecture purposes, to be confirmed by MRG's actual counsel before use.**

- **UC-1, UC-2:** classified here as **limited-risk** (transparency obligations), not one of the Act's Annex III high-risk categories — marketing content/claims review isn't an enumerated high-risk use, and mandatory human sign-off means the AI never makes an autonomous decision with legal effect. **This classification is conditional, not permanent: if MRG ever removed the mandatory human sign-off and let either use case auto-publish, the classification would need re-assessment and would likely escalate.** The human-in-the-loop requirement in this document isn't just internal risk management — it's what keeps these use cases out of the Act's higher-obligation tier.
- **UC-3:** **minimal risk** under the Act — an internal narrative over aggregated data, no external audience, no legal effect. Still held to this document's Tier 2 governance regardless, since MRG's own risk tolerance is the binding constraint here, not the Act's floor.

## DPIA-lite — UC-3 (lifecycle/CRM use case)

- **Purpose:** generate an internal performance narrative from aggregated segment and engagement data.
- **Data processed:** aggregated, suppressed segment counts and engagement rates only, per [D5](05-data-pipelines.md)'s `lifecycle-segment-feed` contract — no row-level customer data.
- **Necessity and proportionality:** aggregation is both the privacy-protective choice and the functionally sufficient one — narrative synthesis doesn't need row-level data to do its job, so there's no proportionality trade-off to make here; the minimal-data option and the sufficient option are the same option.
- **Third-party exposure:** yes — the aggregated data crosses [D4](04-target-architecture.md)'s TB2→TB3 boundary as part of the inference prompt. By contract, nothing that crosses is individually re-identifiable given the 50-member suppression floor.
- **Residual risk — the mosaic/differencing effect:** the 50-member suppression floor protects any single report, but repeated reporting across cycles has a known residual risk: if a segment's `reachable_count` moves from 48 (suppressed in one cycle) to 52 (shown in the next), the *difference* reveals that roughly four people changed status between cycles — a small but real re-identification vector that a static per-report threshold doesn't close. **This is not yet solved in `lifecycle-segment-feed` v1.0.0.** Recommended follow-up: Legal & Compliance and Data Engineering jointly define a minimum-delta suppression rule in a future contract version. Flagging this as an open residual risk is more honest than claiming the current suppression floor fully closes it, because it doesn't.

## Vendor risk criteria

Applies to the model provider (D4's TB3) and to any vendor engaged per [D8](08-vendor-evaluation.md)'s buy decisions (currently Vendor A, for UC-2):

| Criterion | Requirement |
|---|---|
| **Residency** | Contractual commitment to process and store MRG data only in specified regions, matching [D4](04-target-architecture.md)'s deployment region |
| **Subprocessors** | Vendor must disclose all subprocessors in advance, with MRG's right to object to new ones before they're added |
| **Training-data usage** | Explicit contractual guarantee that MRG's submitted content is never used to train or fine-tune models for other customers' benefit — opt-out enforced by default in the contract, not offered as an opt-in setting |
| **Exit** | Guaranteed data egress in a usable format, a defined transition-assistance period, and deletion certification after exit — see [D8](08-vendor-evaluation.md)'s lock-in analysis for why this matters concretely for Vendor A |

## Model/prompt change control

1. Every production prompt is versioned in a prompt registry — no in-place edits to a live prompt.
2. A prompt or model-version change must re-run against a fixed evaluation set before promotion — the same eval-portability point [D8](08-vendor-evaluation.md) raises as a lock-in criterion applies internally too: an eval set that only works against one model version isn't actually testing anything.
3. Policy-engine rule changes (the actual governance logic, not the prompt) go through a stricter path than prompt changes: Legal & Compliance sign-off required, mirroring [D5](05-data-pipelines.md)'s requirement that changes touching `lifecycle-segment-feed`'s suppression boundary need the same sign-off.
4. Every promotion requires a documented rollback plan before it ships, not written after something breaks.

## Incident path

An incident is: an unsubstantiated claim shipped externally despite Tier 1 review, a suppression-floor breach in the metrics store, or a policy-engine fail-open event (the engine should never fail open per [D7](07-nfr-budgets.md) — an occurrence of one is itself the incident, independent of whether it caused visible harm).

1. **Contain:** pull the specific prompt or rule version involved; this is why every version is a named, rollback-able artifact per the change-control policy above.
2. **Notify:** Legal & Compliance and the affected brand or regional team, immediately — not after root cause is known.
3. **Post-mortem:** required for every incident, no severity threshold below which it's skipped.
4. **Close the loop:** if the post-mortem reveals a gap in this document or in a D5 data contract, that document is updated as part of closing the incident, not filed as a separate future task.

## What this changes

This is the document Legal & Compliance signs off against before any of the three use cases moves from spec to build. The conditional EU AI Act classification above is the strongest single constraint in this file: it means the mandatory human sign-off in the Tier 1 HITL policy is not a design preference that could be relaxed later for speed — relaxing it changes the use case's actual legal classification, not just its internal risk posture.
