# Executive Brief

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** CMO and marketing leadership. No technical background assumed.

## The problem

Getting a campaign from brief to launch takes about 23 business days today `[illustrative]`. Roughly 60% of that time isn't spent doing work — it's spent waiting in a queue, mostly for legal review and for translating and re-clearing campaigns across our four markets. That's not a people problem; it's a handoff problem, and it's been getting worse as we've added markets without adding review capacity to match.

## What we're proposing

Three narrow, specific places where a first automatic check catches obvious issues before they reach a person — not instead of a person:

1. **A first check on campaign copy**, before it goes to Brand and Legal, that flags language likely to need substantiation (things like "clinically proven" or "guaranteed results") so reviewers spend their time on real judgment calls, not repeat catches of the same known issues.
2. **The same kind of first check for translated copy**, since a phrase that was fine in English can become a legal problem once translated, and today that's only caught the second time it goes through legal review in each market.
3. **An automatic first draft of our performance readouts**, pulling together the numbers we already collect so the team spends its time interpreting results, not assembling the same report by hand every cycle.

**What doesn't change: nobody's judgment gets replaced.** Every flagged item still goes to a person — the same Brand and Legal reviewers who look at it today. The system's job is to make sure the easy, repeatable issues get caught earlier, not to make the call on anything that actually matters. We tested this specifically: a product with real clinical backing clears the check; a product without it gets flagged, every time.

## Three decisions we're making now

- **We're drawing a hard line between "flag for a person" and "decide for the company," and we're not moving that line for speed.** Legal sign-off on claims and Brand's judgment on creative fit stay fully human, always — not because the technology can't attempt it, but because the accountability for getting it wrong belongs to a named person, not a system.
- **We're building the two pieces closest to our own brand ourselves, and buying the one piece that's really a legal-research problem.** Keeping up with advertising law across four markets, indefinitely, is a specialist's job — we're using an outside vendor who does that as their core business, rather than growing that expertise in-house. The other two pieces stay close to our own data and brand voice, so we're building those ourselves.
- **We're asking IT/Platform to invest in shared infrastructure, not just this one project.** Three of the things this project had to build from scratch — a proper way to receive creative briefs, a shared way to check what customer data is safe to use, and a single shared connection to the AI vendor we use — will be needed again by the next team that wants to do something similar. Fixing them once, centrally, is cheaper than every team solving them separately.

## What this costs, and what we're accepting

At our current size, the recommended approach costs roughly **$1.0M over three years** `[illustrative]`, in the same range as either buying everything from a vendor or building everything ourselves — cost isn't what decided this; which pieces are worth owning is. Buying everything looks cheaper at a small pilot scale but gets more expensive than building as we grow across more markets; we've flagged the point at which that trade-off would need revisiting if we expand faster than planned.

The risk we're explicitly accepting: the automatic checks won't catch everything, which is exactly why the human review step isn't going anywhere. The risk we're explicitly not accepting: letting anything ship without that review, no matter how confident the system is. If the system itself has a problem, it's built to hold everything for review rather than wave things through — a cautious failure, not a permissive one.

## What this brief asks for

Approval to build against this plan as scoped, and a green light to bring the platform-investment ask to IT/Platform leadership as a separate, smaller conversation — it doesn't block this project, but it's what makes the next one faster.
