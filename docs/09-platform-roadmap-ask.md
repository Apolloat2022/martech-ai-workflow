# Platform Capability Gaps & Roadmap Ask

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Platform engineering leadership — a roadmap owner outside marketing, with its own priorities and competing asks.

This is the gap-closer document for "influence platform roadmaps and identify gaps in infrastructure or tooling." It's written as an investment proposal, not a mandate: marketing doesn't own platform engineering's roadmap, and every ask below is scoped, sequenced, and justified by business impact rather than presented as a foregone conclusion.

## Why this is platform engineering's problem, not marketing's

Building [D4](04-target-architecture.md)'s architecture surfaced four gaps that this platform worked around rather than solved, because working around them was in scope for one team's one project and fixing them properly isn't. Every one of the four will be hit again — by this platform's own future use cases, and by the next team at MRG that tries to build anything AI-adjacent. That recurrence is the argument for platform ownership: a gap one team routes around once is a workaround; a gap every team routes around independently is a missing platform capability.

## Capability inventory

| Capability | Status | Notes |
|---|---|---|
| Managed compute platform (VPC, ECS Fargate, networking) | **Have** | Already the foundation D4's deployment view builds on |
| Secrets management | **Have** | Used as designed in D4 |
| Observability/tracing baseline | **Have** | CloudWatch + X-Ray exist, though the AI-specific trace shape ([D6](06-interface-spec.md)'s `TraceInfo`) is this platform's own addition, not a shared capability yet |
| CI/CD and infra-as-code patterns | **Have** | Standard org practice, reused here without modification |
| Data contract registry / breaking-change process | **Partial** | [D5](05-data-pipelines.md) defined two contracts with a real deprecation policy, but there's no platform-wide registry another team's contracts are discoverable in — this platform's contracts are only known to whoever reads this repo |
| Governed brief/creative intake with a real API | **Absent** | Gap 1 |
| Consent/purpose-check service for lifecycle data | **Absent** | Gap 2 |
| Centralized model-provider gateway | **Absent** | Gap 3 |
| Shared retrieval/ingestion-as-a-service | **Absent** | Gap 4 |
| AI-specific cost/usage tracking (FinOps) | **Absent** | Downstream of Gap 3 — no broker means no consolidated spend visibility |

## The four gaps

### Gap 1 — No governed, API-accessible brief/creative intake

**Impact.** [D3](03-data-landscape.md) flagged two separate symptoms of the same root cause: the ticketing system's briefs are free text with unreliable webhooks ([D2](02-bottleneck-register.md) B-04), and the agency file share has no API, no versioning, and no MRG governance visibility at all — the one system in the entire landscape [D5](05-data-pipelines.md) had to exclude from pipelining outright rather than work around. Every future use case that touches brief or creative intake inherits this same gap and will build its own patch, the way this platform built a webhook-plus-hourly-reconciliation hybrid because the source couldn't be trusted on its own.

**Proposed owner:** Platform Engineering (a shared intake/workflow service is core infrastructure; no single marketing sub-team should own the system every future AI use case depends on).

**Sequenced ask:**

1. *0–2 quarters:* add a versioned, reliable API and guaranteed-delivery eventing to the existing ticketing system — the smaller, cheaper half of this gap.
2. *2–4 quarters:* bring the agency file share under a governed submission surface — either a lightweight intake API MRG owns, or a data-processing agreement with the agency's own tooling vendor that guarantees API-level access MRG can build against.

### Gap 2 — No consent/purpose-check service for lifecycle data

**Impact.** [D3](03-data-landscape.md) flagged consent state as the single highest-sensitivity field in the landscape, and [D5](05-data-pipelines.md)'s entire `lifecycle-segment-feed` contract exists as a bespoke, one-off workaround — a hand-built aggregation-and-suppression boundary — because no shared service exists that a use case could simply call to ask "is this data cleared for this purpose." Every future use case touching lifecycle or CDP data will otherwise re-invent its own version of that suppression logic, at the quality level of whichever team happens to build it that time.

**Proposed owner:** Platform Engineering, jointly with Data Governance (shared infrastructure with a compliance-owned rule set).

**Sequenced ask:**

1. *0–2 quarters:* define a purpose-tagging schema on top of the CDP's existing consent fields — a data-modeling exercise more than an engineering one.
2. *2–4 quarters:* expose it as a queryable service other teams call directly, rather than each team re-deriving its own aggregation and suppression rules the way this platform had to.

### Gap 3 — No centralized model-provider gateway

**Impact.** [D4](04-target-architecture.md)'s architecture integrates directly with a single third-party model provider. If the next team at MRG builds its own AI use case, it will build its own direct provider integration too — its own auth, its own rate-limiting, its own cost tracking, and its own trust-boundary review from scratch. That doesn't scale past a second team: it produces duplicated engineering effort, inconsistent enforcement of exactly the kind of PII boundary [D5](05-data-pipelines.md) was careful about, and zero consolidated visibility into what MRG is spending on inference across the business.

**Proposed owner:** Platform Engineering (textbook shared infrastructure — this is the kind of gap a platform team exists to close before it multiplies).

**Sequenced ask:**

1. *0–2 quarters:* a thin centralized proxy for model-provider calls, with centralized key management and basic cost tracking — deliberately not full-featured at first.
2. *2–4 quarters:* migrate this platform's own gateway to call through the broker instead of the provider directly, and offer it as the sanctioned integration path for the next team, so the second AI initiative at MRG doesn't repeat this platform's one-off integration work.

### Gap 4 — No shared retrieval/ingestion-as-a-service

**Impact.** This platform built its own retrieval index, and made its own chunking, embedding, and ingestion-mode decisions ([D5](05-data-pipelines.md)) from scratch. A future team building a different retrieval-augmented use case has no shared infrastructure to build on and will re-derive the same class of decisions — including, if they're less careful than this document was, the PII-exclusion discipline that kept S3/S4 out of the retrieval index entirely.

**Proposed owner:** Platform Engineering, with Data Engineering co-owning the ingestion-pattern side.

**Sequenced ask:**

1. *0–2 quarters:* publish this platform's ingestion and chunking patterns ([D5](05-data-pipelines.md)) as a reference architecture — cheap, and immediately useful to the next team even before any new infrastructure exists.
2. *2–4 quarters:* if a second retrieval-augmented use case materializes within roughly two to three quarters, invest in generalizing the ingestion workers into an actual shared service rather than letting a second one-off get built.

## What this changes

Each gap has a cheap, low-commitment first step (quarters 0–2) and a costlier second step gated on a specific trigger (a second use case, a specific timeline), rather than a single expensive ask up front — the sequencing itself is the pitch: platform engineering can fund the first step of all four gaps without committing to the second step of any of them until the trigger condition is real. If none of these gaps are addressed, every future AI use case at MRG will re-pay the same integration tax this one did, one team at a time.
