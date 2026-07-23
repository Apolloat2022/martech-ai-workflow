# 0012. No speculative multi-tenancy; single-tenant until a second tenant is real

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D6](../06-interface-spec.md)'s `invoke` request schema needed a decision on tenancy. MRG is a single organization today, but enterprise platforms often anticipate a future acquisition, brand split, or second business unit by reserving a `tenant_id` field from day one, even while unused, to avoid a breaking change later.

## Decision Drivers

- [PROJECT_PLAN.md](../../PROJECT_PLAN.md) section 6 places multi-tenancy implementation explicitly out of scope.
- A reserved-but-unused field is speculative complexity: it has to be documented, explained to every new engineer, and maintained as dead weight until (if ever) it's needed.

## Considered Options

- Single-tenant now; add tenancy as a new major version if and when a second tenant becomes real (chosen)
- Reserve an optional, unused `tenant_id` field now, to avoid a breaking change later
- Design a full multi-tenant isolation layer now, anticipating enterprise scale

## Decision Outcome

Chosen option: single-tenant, with no reserved field. A future multi-tenant need is exactly the kind of hypothetical requirement this repo's engineering discipline argues against designing for speculatively — if MRG ever needs a second tenant, that need will have actual shape (isolation model, data residency per tenant, billing) that a field reserved today cannot predict correctly anyway. [D6](../06-interface-spec.md)'s versioning policy already has a defined path for a breaking change (30 days' notice, 60-day deprecation window) — multi-tenancy would use that path when and if it's real, rather than a speculative field carried unused from day one on the chance it might be needed.

### Consequences

- Good, because the API surface stays exactly as complex as MRG's actual, current organizational shape, with nothing to explain that doesn't do anything yet.
- Bad, because a genuine future multi-tenancy need becomes a breaking `/v2` change instead of an additive one — accepted deliberately, on the basis that a field reserved without knowing the real isolation requirements would likely need to change shape anyway, making the "avoided" breaking change illusory.

## Links

- [D6 — Interface & Integration Spec](../06-interface-spec.md), "Tenancy"
- [PROJECT_PLAN.md](../../PROJECT_PLAN.md), section 6, "Explicitly out of scope"
