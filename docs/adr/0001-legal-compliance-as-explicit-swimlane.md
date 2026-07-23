# 0001. Draw Legal & Compliance as its own swimlane despite sitting outside marketing headcount

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

MRG's marketing org (~120 people) sits in five groups: Product Marketing, Brand, Lifecycle/CRM, Regional Field Marketing, and the external creative agency. Legal & Compliance is a shared corporate function, not part of that headcount. [D1](../01-current-state-process-map.md)'s process map needed a lane structure — should Legal & Compliance get its own lane, or should its review step be folded into an adjacent marketing lane to keep the swimlane strictly to "marketing's five teams"?

## Decision Drivers

- The map has to represent where time actually goes, not just who's on the marketing org chart.
- Legal & Compliance owns two of the largest queues in the process (the claims-review and localized-claims-re-review handoffs).

## Considered Options

- Draw Legal & Compliance as its own lane (chosen)
- Fold claims review into Brand's lane, since Brand hands off to Legal in the current process

## Decision Outcome

Chosen option: draw Legal & Compliance as its own lane, because folding it into Brand's lane to preserve a clean "five marketing teams" swimlane would hide exactly the two queues [D2](../02-bottleneck-register.md) later identifies as the largest sources of cycle time. A process map that flatters the org chart at the expense of showing where the 23 business days `[illustrative]` actually goes is decoration, not analysis.

### Consequences

- Good, because every later document that cites a Legal & Compliance handoff by ID (H4, H5, H6, H7, H8) has an honest, distinct lane to point at.
- Bad, because the swimlane now has six lanes instead of five, and a reader expecting "the five marketing teams" has to be told why a sixth, non-marketing lane appears — handled with one explanatory paragraph in D1 rather than silently.

## Links

- [D1 — Current-State Process Map](../01-current-state-process-map.md)
