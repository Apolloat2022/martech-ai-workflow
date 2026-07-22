# Vendor Evaluation & Build-vs-Buy

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Procurement, platform engineering, marketing technology leadership.

**A note on vendor names:** this document uses labeled archetypes (Vendor A, Vendor B) rather than named real products. A capability comparison against real vendors' current published pricing and feature sets would need to be re-verified at the point of actual procurement regardless of what's written here today — vendor capabilities move faster than this document's shelf life. Naming specific real companies with claims that go stale within a quarter would create false confidence; the archetypes below are stable categories (a specialized content-governance SaaS, a generalist enterprise AI platform) that the underlying judgment holds up against even as specific vendors' offerings change.

## The rubric

Same six criteria and weights, applied to all three use cases from [D4](04-target-architecture.md). Weights are justified here, before any score appears below.

| Criterion | Weight | Why this weight |
|---|---|---|
| Governance & data-residency fit | 25% | The highest weight, deliberately. A governance failure against [D3](03-data-landscape.md)'s PII flags or [D4](04-target-architecture.md)'s trust boundaries isn't a score deduction — it's a veto Legal & Compliance would exercise regardless of how well an option scores elsewhere. |
| Task fit / quality for this use case | 20% | The actual point of the exercise, but not weighted highest: most credible options today clear a "good enough" bar for these three task shapes, so the real differentiator tends to be risk, cost, or lock-in rather than raw capability. |
| Integration effort with D5/D6 | 15% | This platform already has an ingestion pipeline and a gateway contract. The fastest path to value is whichever option fits that contract with the least new adapter work. |
| Total cost of ownership (3-year) | 15% | See the TCO model below — weighted equally with integration effort because upfront integration cost and ongoing cost trade off against each other, not additively. |
| Lock-in / portability | 15% | Switching cost matters as much as day-one cost for a platform meant to serve MRG for years, not one campaign cycle. |
| Ongoing operational burden | 10% | Lowest weight, not because it doesn't matter, but because platform engineering headcount for this is fixed regardless of use case — it constrains what's feasible more than what's optimal. |

Weights sum to 100%. Options scored 1–5 per criterion.

## UC-1 — Claims & Brand Pre-Screen Assistant

| Option | Governance (25%) | Task fit (20%) | Integration (15%) | TCO (15%) | Lock-in (15%) | Ops burden (10%) | **Weighted total** |
|---|---|---|---|---|---|---|---|
| Build | 5 | 4 | 5 | 3 | 5 | 3 | **4.30** |
| Vendor A (content-governance SaaS) | 3 | 5 | 2 | 4 | 2 | 4 | 3.35 |
| Vendor B (generalist AI platform) | 4 | 3 | 3 | 3 | 3 | 4 | 3.35 |

**Verdict: Build.** This use case needs deep, ongoing integration with MRG's own brand corpus and claims taxonomy (D5's `dam-asset-feed` contract) — content that's core to MRG's differentiation, not a commodity. Vendor A scores highest on task fit (purpose-built for this) but loses on governance and lock-in: it requires exporting MRG's brand/claims content into the vendor's proprietary index, which is a new trust-boundary crossing [D4](04-target-architecture.md) doesn't currently draw, and the resulting rule encoding isn't portable back out.

## UC-2 — Localization Claims Consistency Checker

| Option | Governance (25%) | Task fit (20%) | Integration (15%) | TCO (15%) | Lock-in (15%) | Ops burden (10%) | **Weighted total** |
|---|---|---|---|---|---|---|---|
| Build | 3 | 2 | 5 | 2 | 5 | 2 | 3.15 |
| Vendor A (content-governance SaaS) | 3 | 5 | 3 | 4 | 2 | 4 | **3.50** |
| Vendor B (generalist AI platform) | 4 | 2 | 3 | 3 | 3 | 4 | 3.15 |

**Verdict: Buy (Vendor A).** Note Build's governance score here (3) is deliberately lower than its UC-1 score (5) — not inconsistent scoring, a different risk. For UC-2, "governance" also has to account for the *currency and correctness* of self-maintained, multi-market legal claims rules, not just data residency. A stale or wrong in-house ad-law interpretation is itself a compliance failure. Maintaining accurate claims rules across four (and growing) markets indefinitely is a specialized, ongoing legal-research burden — exactly the kind of capability a vendor whose core business is maintaining that library across many customers is structurally better positioned to carry than MRG's own small team. This is the one use case in this document where buying wins, and it wins for a reason specific to what the task actually requires, not because Vendor A is generically superior.

## UC-3 — Performance Readout Synthesis

| Option | Governance (25%) | Task fit (20%) | Integration (15%) | TCO (15%) | Lock-in (15%) | Ops burden (10%) | **Weighted total** |
|---|---|---|---|---|---|---|---|
| Build | 5 | 4 | 5 | 5 | 5 | 4 | **4.70** |
| Vendor A (content-governance SaaS) | 3 | 2 | 2 | 2 | 2 | 3 | 2.35 |
| Vendor B (generalist AI platform) | 4 | 4 | 3 | 3 | 3 | 4 | 3.55 |

**Verdict: Build.** The clearest call of the three. This is a low-differentiation summarization task over data MRG already owns and has already paid to aggregate ([D5](05-data-pipelines.md)'s `lifecycle-segment-feed`). Paying a vendor subscription — and handing that data to a third party — for a task an in-house model call handles at a fraction of the cost is a straightforward loss on every criterion except task fit for Vendor B, which isn't enough to close a gap this wide.

Two Build verdicts and one Buy verdict: the rubric is doing real work, not producing a foregone conclusion. If every use case had come back the same way, that would be the signal to distrust the rubric, not the use cases.

## TCO model, three volume tiers

Three strategies compared, not per-use-case but as whole-portfolio choices, at three illustrative volume tiers. All figures `[illustrative]`, order-of-magnitude, 3-year totals.

| Tier | Profile |
|---|---|
| **Tier 1 — Pilot** | 20 campaigns/month, 1 market |
| **Tier 2 — Current MRG scope** | 150 campaigns/month, 4 markets (matches the architecture as designed throughout this repo) |
| **Tier 3 — Post-expansion** | 400 campaigns/month, 8 markets (illustrative growth scenario) |

| Strategy | Tier 1 (3yr) | Tier 2 (3yr) | Tier 3 (3yr) |
|---|---|---|---|
| All-Build (UC-1, UC-2, UC-3 all in-house) | $525K | $1,080K | $1,950K |
| All-Buy (all three via vendor) | $390K | $1,050K | $2,190K |
| **Recommended mixed** (Build UC-1+UC-3, Buy UC-2) | $455K | $1,040K | $1,970K |

**The recommendation isn't the cheapest option at every tier, and that's a finding, not an inconsistency.**

- **At Tier 1 (pilot),** all-buy is cheapest in raw terms — fixed build costs dominate at low volume, and a short pilot shouldn't carry the sunk cost of a full in-house build before demand is proven. If MRG were only ever running a single-market pilot, buying everything would be the defensible call.
- **At Tier 2 (current scope),** the three strategies land within about 4% of each other. Cost alone doesn't decide it here — the governance and lock-in reasoning from the weighted matrices above does, which is why the recommendation is mixed, not whichever raw number is lowest.
- **At Tier 3 (post-expansion), the recommendation's advantage over all-build narrows and nearly inverts.** UC-2's in-house legal-research cost grows *sub-linearly* with each additional market once a research function already exists (a market-8 review leans on tooling and precedent a market-1 review had to build from scratch), while Vendor A's subscription fee for UC-2 scales roughly linearly with markets and volume. **This is a real crossover, not a rounding error: the Buy verdict for UC-2 is scoped to MRG's current, roughly four-market footprint. If MRG expects to reach Tier 3 within this model's amortization horizon, that is the trigger to revisit the UC-2 vendor decision — not a permanent commitment made independent of scale.**

## Lock-in analysis

| Dimension | Build | Buy (Vendor A, UC-2) |
|---|---|---|
| **Switching cost** | Near-zero for a model-provider swap — see D4's Azure equivalence table; the model catalogue, not the application code, is what would need re-validating. | Real and significant: illustrative one-time cost of $150–250K `[illustrative]` to exit and rebuild UC-2 in-house, dominated by re-encoding the vendor's proprietary multi-market claims-rule format into an MRG-owned one, not by engineering effort. |
| **Data egress** | N/A — data never leaves MRG's environment except the same de-identified inference call every use case makes. | Must be a contractual requirement, not assumed: MRG's submitted content and the vendor's flagging history must be exportable in a usable format on exit. This is a mandatory term in any Vendor A contract, tied to [D10](10-governance.md)'s vendor exit criteria. |
| **Prompt / eval portability** | Fully MRG-owned artifacts, portable across any model-provider swap by design (the same model-abstraction interface the reference slice implements). | Not portable. The vendor's rule logic lives inside their platform; this is the actual lock-in, more than the underlying data itself. |

This is the same argument [D4](04-target-architecture.md) made about AWS-versus-Azure infrastructure, one layer up: the model or vendor catalogue is what's expensive to leave, not the surrounding scaffolding.

## What this changes

The recommendation — build UC-1 and UC-3, buy UC-2 from a specialized vendor — sets what D9's platform-engineering roadmap ask has to support (a model-provider integration path for the two built use cases, and a governed vendor-integration pattern for the one bought use case) and what D10's vendor risk criteria apply to concretely (Vendor A is the vendor D10's residency/subprocessor/exit checklist is written against, not a hypothetical). The Tier 3 crossover is a standing item for whoever owns this platform after MRG's next market expansion — it should be re-run against real numbers before it's assumed to still hold.
