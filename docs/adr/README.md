# Architecture Decision Records

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Engineering and architecture decision-makers who need the reasoning behind a design choice, not just the choice itself.

ADRs in this directory follow the [MADR](https://adr.github.io/madr/) format, numbered `NNNN-short-title.md`. They are retro-written against decisions already taken across D1–D10 — each one documents a choice that was made while writing those documents, with the alternative that lost and why, not a decision invented after the fact to pad the count.

| ID | Title | Rejects the obvious AI answer? |
|---|---|---|
| [0001](0001-legal-compliance-as-explicit-swimlane.md) | Draw Legal & Compliance as its own swimlane despite sitting outside marketing headcount | |
| [0002](0002-no-automated-claims-signoff.md) | Decline to automate claims sign-off itself | **Yes** |
| [0003](0003-no-automated-brand-review-calibration.md) | Decline to automate brand-review calibration | **Yes** |
| [0004](0004-no-ai-for-legal-review-capacity.md) | Decline to treat legal-review capacity as an AI problem | **Yes** |
| [0005](0005-scope-exactly-three-ai-use-cases.md) | Scope exactly three AI use cases; solve the rest without a model | **Yes** |
| [0006](0006-exclude-pii-sources-from-retrieval-index.md) | Exclude PII-flagged sources from the retrieval index; pre-aggregate instead | |
| [0007](0007-reject-cdc-for-pim-feed.md) | Reject CDC for the PIM feed; use daily batch | |
| [0008](0008-hybrid-ingestion-for-ticketing-source.md) | Use hybrid webhook-plus-reconciliation ingestion for the ticketing source | |
| [0009](0009-target-aws-not-azure.md) | Target AWS, not Azure, for the deployment view | |
| [0010](0010-mixed-build-vs-buy-portfolio.md) | Adopt a mixed build-vs-buy portfolio rather than a uniform strategy | |
| [0011](0011-policy-engine-fails-closed.md) | Fail closed, not open, on policy-engine unavailability | |
| [0012](0012-no-speculative-multi-tenancy.md) | No speculative multi-tenancy; single-tenant until a second tenant is real | |

Four ADRs (0002–0005) reject the obvious AI answer — more than the minimum of three, because this repo's central argument is that judgment about where *not* to apply AI is the load-bearing skill, not a footnote.

## What this changes

An ADR here is the citable reason behind a choice already reflected in D1–D10 — if a future reviewer or a future engineer asks "why doesn't this platform just use CDC everywhere" or "why is there a human in the loop on claims review," the answer is one of these records, not a re-argued conversation. Changing any decision below means superseding its ADR explicitly (a new ADR with `Status: Supersedes 000N`), not quietly editing the source document it was made for.
