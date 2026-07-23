# 0003. Decline to automate brand-review calibration

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Date:** 2026-07-22
**Status:** Accepted

## Context and Problem Statement

[D2](../02-bottleneck-register.md) (B-09) identifies that brand review outcomes vary depending on which reviewer is assigned — the same creative can pass or fail based on individual taste, with no shared calibration rubric. This looks automatable: a model could, in principle, score creative against brand guidelines consistently, removing reviewer-to-reviewer variance entirely.

## Decision Drivers

- Brand fit is a subjective, high-context judgment about creative quality, not a rule-following task.
- The retrieval-backed brand-guideline assistant already scoped for B-03 (surfaced to the agency *during* drafting) is a different, narrower tool than a model that scores or gates brand review itself.

## Considered Options

- No automation of the review verdict; fix reviewer inconsistency with a calibration rubric and reviewer rotation (chosen)
- An AI brand-fit scoring model that reviewers must justify overriding
- An AI brand-fit scoring model that auto-clears above a threshold, mirroring the (rejected) approach considered for claims sign-off

## Decision Outcome

Chosen option: no automation of the verdict itself, because AI assistance here either rubber-stamps whatever bias already exists in the training signal (past reviewer decisions, which is exactly the inconsistency being complained about) or oversimplifies brand taste into a checklist that loses the judgment brand review exists to apply. The actual fix — a calibration rubric and reviewer rotation — is a management and process intervention. Recommending a model here would be recommending automation of a problem that isn't a technology problem, which is precisely the failure mode [D2](../02-bottleneck-register.md)'s register was built to catch.

### Consequences

- Good, because this keeps the platform's scope honest about what AI is actually good for — B-03's retrieval assistant (helping the agency find and apply the guideline that matters) survives this decision; a verdict-scoring tool does not.
- Bad, because reviewer-to-reviewer inconsistency remains a live cost ([D2](../02-bottleneck-register.md) B-03's rework loop) that this platform does not reduce — it is explicitly out of scope for this repo to also redesign brand review's management practices.

## Links

- [D2 — Bottleneck & Redundancy Register](../02-bottleneck-register.md), rows B-03 and B-09
