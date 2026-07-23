# 0005. Scope exactly three AI use cases; solve the rest without a model

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D2](../02-bottleneck-register.md) scored seven handoffs High or Medium automation candidacy: B-01, B-02, B-03, B-04, B-05, B-06, B-07. [D4](../04-target-architecture.md) had to decide how many of these become AI use cases in the target architecture, versus how many are better solved with conventional tooling that happens to involve no model at all.

## Decision Drivers

- "High automation candidacy" in [D2](../02-bottleneck-register.md) means "worth automating," not "worth building a model for" — the register never claimed every High row needs AI specifically.
- A form-validation problem (B-04) and a metadata-templating problem (B-05) don't get *better* with a model in the loop; they get an unnecessary dependency, a new failure mode, and a governance review they didn't need.

## Considered Options

- Three AI use cases (UC-1, UC-2, UC-3), with B-04/B-05/B-06 solved as deterministic pipeline/tooling fixes (chosen)
- Seven AI use cases, one per High/Medium row, for architectural completeness
- A single general-purpose "marketing AI assistant" covering all seven rows through one flexible interface

## Decision Outcome

Chosen option: three AI use cases. B-04 (missing brief fields) is a structured-form problem — required-field validation needs no model. B-05 (per-market asset re-tagging) is a mechanical metadata transform from a source asset's existing tags plus a market code — templating, not judgment. B-06 (activation-timing coordination) needs a shared calendar, not reasoning about content. Building AI for any of these would be over-applying the technology exactly where [D2](../02-bottleneck-register.md) already flagged the simpler fix as sufficient — the same discipline that produced B-08/B-09/B-10's "None" rows, applied to the High/Medium side of the register instead of the None side. A single do-everything assistant was rejected for a related reason: it would blur [D10](../10-governance.md)'s risk tiering, since B-04/B-05/B-06's tooling fixes carry none of UC-1/UC-2's regulatory exposure and shouldn't inherit its governance overhead.

### Consequences

- Good, because [D4](../04-target-architecture.md)'s architecture stays a small, defensible vertical slice instead of a seven-use-case platform, matching the repo's ~70/30 artifacts-to-code ratio.
- Bad, because B-04/B-05/B-06's cycle-time savings ([D2](../02-bottleneck-register.md)'s `[illustrative]` costs, roughly 6.5 business days combined) are left as a stated but unimplemented recommendation — a future team has to actually build the form and the metadata template for that time to be recovered.

## Links

- [D2 — Bottleneck & Redundancy Register](../02-bottleneck-register.md)
- [D4 — To-Be AI Architecture](../04-target-architecture.md), "Which use cases this architecture serves"
