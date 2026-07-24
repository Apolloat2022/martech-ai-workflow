# MAWO — Marketing AI Workflow Orchestration

## Build Plan / Handoff Document

**Author of plan:** Opus 4.8 (planning session)
**Intended executor:** Sonnet (or any coding agent)
**Repo root:** `C:\Workspace\Projects\Marketing-ai-workflow`
**Status:** Complete. All of D1–D14 built, verified, and pushed to `main`; see section 8's Definition of Done.
**Date:** 2026-07-22 (plan authored); completed 2026-07-24

---

## 0. Read this first

This is a **portfolio artifact repository**, not a product. Its job is to be the thing Robin Pandey links in an application for an **AI Solution Architect (Marketing / MarTech)** role, so a hiring manager can see architecture judgment in fifteen minutes.

The target JD's core framing — and therefore this project's core framing — is:

> *"Ensuring marketing's business requirements and enterprise-alignment needs are reflected in that design... **without duplicating the build-side design and development work.**"*

That sentence sets the whole tone. This role **assesses, specifies, validates, and governs**. It does not ship the model. So the primary deliverable is **architecture artifacts**, with a *small* runnable slice attached only to prove the artifacts are executable rather than decorative.

**Ratio to hold: ~70% artifacts, ~30% code.** If you find yourself building a large application, you have drifted off-plan. Stop and re-read this section.

### Two specific gaps this project exists to close

Robin's current CV cannot evidence these two JD requirements. This project is the fix. Treat them as the highest-priority deliverables, not as nice-to-haves:

1. **"Collaborate with Data Engineering teams to design data pipelines"** → closed by Deliverable D5 (pipeline design + lineage + contracts).
2. **"Influence platform roadmaps and identify gaps in infrastructure or tooling"** → closed by Deliverable D9 (capability gap analysis + a written roadmap ask to platform engineering).

If time runs short, cut the runnable slice (Phase 2) before you cut D5 or D9.

**If Phase 2 is cut:** D7 ships with `[illustrative]` budgets only, the README states plainly that the reference slice is specified but not yet built, and DoD items 3 and 4 are struck. Do not fake `[measured]` numbers to satisfy the checklist — a spec-only repo that says so is stronger than one that implies code exists.

### Effort budget

This repo is one line in a job application. It should take **three to four focused days**, not three weeks. Rough page targets, to keep the writing agent honest:

| Deliverables | Target length |
|---|---|
| D1, D2, D3 | ~2 pages each |
| D4, D6, D7, D9, D11 | ~3 pages each (ADRs: ~½ page per ADR) |
| D5, D8, D10 | ~4–5 pages each |
| D14 | 2 pages, hard cap |

These are targets, not quotas. A tight 2-page D5 beats a padded 5-page one. But if a document is running past its target, that is the signal to cut scope, not to keep writing — and if total effort passes four days, apply the cut order in this section.

### Integrity constraints — non-negotiable

- The scenario company is **fictional**. Use **"Meridian Retail Group" (MRG)**, a fictional mid-size omnichannel retailer. Never imply this was a real client engagement.
- Every document must carry this header line: `> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.`
- Do **not** use real vendor logos, real pricing sheets, or scraped proprietary material. Vendor comparisons must use publicly documented capabilities only, and must be dated and marked as "as published, subject to change."
- Do **not** fabricate benchmark numbers. Where a number is illustrative, label it `[illustrative]`. Where it is measured from the runnable slice, label it `[measured]`.

---

## 1. The scenario

**Meridian Retail Group** — fictional omnichannel retailer, ~4,000 employees, marketing org of ~120 across Brand, Product Marketing, Lifecycle/CRM, Regional Field Marketing, and an external creative agency.

**The process under assessment: the campaign content lifecycle.**

Brief intake → creative development → brand review → legal/claims review → localization (4 markets) → asset packaging into DAM → channel activation (email, web, paid social, in-store) → performance readout → next-cycle learning.

**Why this process:** it is dense with exactly the things the JD names — cross-team handoffs, operational dependencies, data flows across disconnected systems, obvious redundancy, and real governance exposure (claims substantiation, brand safety, PII in lifecycle segments, regional privacy divergence). It gives every deliverable something honest to bite on.

**The stated pain (current state):** median 23 business days brief-to-activation `[illustrative]`, with roughly 60% of elapsed time in queue rather than in work — concentrated in legal review and localization.

---

## 2. Deliverables

Each deliverable is a document under `docs/`. Every one must state its **audience** and end with a **"What this changes"** section — one paragraph on the decision it drives. Documents that don't drive a decision are filler; don't write them.

### Phase 1 — Architecture artifacts (the core, do this first)

| ID | Deliverable | File | Notes |
|----|---|---|---|
| **D1** | Current-state process map | `docs/01-current-state-process-map.md` | Mermaid swimlane across the 5 teams + agency. Every handoff numbered H1..Hn. |
| **D2** | Bottleneck & redundancy register | `docs/02-bottleneck-register.md` | Table: ID, handoff ref, symptom, root cause, cycle-time cost `[illustrative]`, automation candidacy (High/Med/Low/None), why. **Include at least three "None" rows** — judgment about where *not* to apply AI is the strongest signal in the whole repo. |
| **D3** | Data landscape assessment | `docs/03-data-landscape.md` | Inventory of ~8 systems (CMS, DAM, CRM/lifecycle, CDP, PIM, analytics, ticketing, agency file share). Per system: owner, data classes, PII flag, quality issues, integration surface (API/webhook/flat file/none), refresh cadence, residency. |
| **D4** | To-be AI architecture | `docs/04-target-architecture.md` | C4 L1 context + L2 container, in Mermaid. Plus a **data flow diagram with explicit trust boundaries** (where PII crosses, where third-party inference happens). Deployment view targets **AWS** (see D4 detail below). |
| **D5** | **Data pipeline & contract design** ⭐ | `docs/05-data-pipelines.md` | **Gap-closer #1.** Ingestion paths into the retrieval layer; CDC vs. batch decision per source and why; chunking/embedding strategy per content type; a **data contract** spec (schema, SLA, ownership, breaking-change policy) for the two highest-value feeds; lineage diagram; the "low-overhead" argument — what you deliberately did *not* pipeline, and why. |
| **D6** | Interface & integration spec | `docs/06-interface-spec.md` + `specs/agent-gateway.openapi.yaml` | OpenAPI 3.1 for the agent gateway: invoke, stream, feedback, health. Auth model, idempotency, error taxonomy, versioning policy, tenancy. |
| **D7** | Non-functional requirements | `docs/07-nfr-budgets.md` | Per use case: p50/p95/p99 latency budget with a **decomposed budget table** (retrieval / inference / rerank / policy check / network), throughput, availability target + error budget, degradation ladder (what fails soft, in what order), resilience posture. |
| **D8** | Vendor evaluation & build-vs-buy | `docs/08-vendor-evaluation.md` | Three use cases, each run through the same rubric. Weighted matrix with **weights justified before scores are shown**. TCO model at 3 volume tiers. Explicit lock-in analysis: switching cost, data egress, prompt/eval portability. **At least one "buy" and at least one "build" conclusion** — a matrix that always says build is not an evaluation. |
| **D9** | **Platform capability gaps & roadmap ask** ⭐ | `docs/09-platform-roadmap-ask.md` | **Gap-closer #2.** Written *to* a platform engineering org. Capability inventory (have / partial / absent), the 4 gaps that block marketing AI at scale, each with business impact, a proposed owner, and a sequenced ask. Written in the register of someone who has to *influence* a roadmap they don't own. |
| **D10** | AI governance framework | `docs/10-governance.md` | Risk tiering for marketing AI use cases; HITL policy **per tier** (who reviews what, when, and what they're accountable for); mapping to NIST AI RMF functions and EU AI Act obligation classes; DPIA-lite for the lifecycle/CRM use case; vendor risk criteria (residency, subprocessors, training-data usage, exit); model/prompt change control; incident path. |
| **D11** | Architecture Decision Records | `docs/adr/NNNN-*.md` | 8–12 ADRs, MADR format. Must include at least three where the decision **rejects** the obvious AI answer. |

#### D4 detail — deployment view and cloud posture

**Decision: the deployment view targets AWS.** Not because AWS is architecturally superior for this workload — it isn't, materially — but because it is where the author's depth actually is, and a deployment diagram that can't survive follow-up questions is worse than no deployment diagram. State that reasoning in one line in the document; a reviewer respects a defensible choice more than a neutral one.

Diagram: one Mermaid deployment view showing VPC layout, where the gateway runs, where the retrieval layer and vector store sit, where inference calls exit to a third party, and which trust boundary each crossing traverses. It must be consistent with the D4 data-flow diagram's boundaries — same crossings, same names.

Then a short **Azure equivalence table** immediately after it, so "we're a Microsoft shop" costs one paragraph rather than a shrug. Map the components actually in the diagram — roughly:

| Concern | AWS (as drawn) | Azure equivalent | Notes / where the mapping frays |
|---|---|---|---|
| Compute (gateway) | ECS Fargate | Container Apps | Near-equivalent |
| Managed inference | Bedrock | Azure OpenAI / AI Foundry | Model catalogues differ — this is the real switching cost, not the compute |
| Vector / retrieval | OpenSearch Serverless | AI Search | Hybrid-search semantics differ |
| Object storage | S3 | Blob Storage | Equivalent |
| Secrets | Secrets Manager | Key Vault | Equivalent |
| Eventing / CDC | EventBridge + DMS | Event Grid + Data Factory | Equivalent in shape, different operational model |
| Identity | IAM roles | Entra ID + managed identities | Equivalent |
| Observability | CloudWatch + X-Ray | Monitor + App Insights | Equivalent |

Adjust rows to match what the diagram actually contains — do not list services the architecture doesn't use. The fourth column is the point of the table: **name at least two places where the mapping is not clean.** A table where everything maps one-to-one reads as a lookup someone pasted; naming the friction is what shows the author has actually moved a workload between clouds. The managed-inference row is the honest one — model availability, not infrastructure, is what makes this migration expensive, and saying so connects the table back to D8's lock-in analysis.

Keep the whole block inside D4's ~3-page target. It is one diagram, one table, and two short paragraphs — not a cloud migration study.

### Phase 2 — Runnable reference slice (proves the specs are real)

Keep this **small**. One vertical slice, not a platform.

**D12** — `reference-slice/`: a FastAPI agent gateway implementing a subset of `agent-gateway.openapi.yaml`, demonstrating:

- Provider-agnostic model abstraction (an interface + two adapters; one may be a deterministic mock so the repo runs with zero API keys)
- Retrieval over a small seeded corpus of fictional MRG brand/claims documents
- A **policy check step** that enforces one governance rule from D10 (e.g. unsubstantiated-claim detection routing to human review) — this is the most important part of the slice, because it's what makes the governance doc credible
- Structured trace output per request: stage timings, model/version, retrieved doc IDs, policy verdict
- A latency harness that emits real numbers to compare against D7's budgets, written to `docs/07-nfr-budgets.md` as `[measured]`

**Hard constraints on the slice:**

- Runs with `docker compose up` **and** with zero external API keys (mock provider default)
- No auth service, no user management, no frontend framework, no database beyond the vector store and SQLite
- If it exceeds ~800 lines of Python, you have overbuilt
- **No standalone vector store container.** The corpus is a dozen or so fictional documents; a separate service is machinery the slice does not earn. Use SQLite with a vector extension, or plain in-memory cosine similarity over deterministic mock embeddings. `docker compose up` should bring up one service. Note the simplification in D4 as a deliberate reference-implementation choice, distinct from what the target architecture specifies at production scale — the gap between the two is itself worth one paragraph.

### Phase 3 — Presentation

**D13** — `README.md`: the fifteen-minute path. Scenario in 3 sentences → the architecture diagram → four "if you only read one thing" links (D2, D5, D8, D9) → how to run the slice → explicit scope disclaimer.

**D14** — `docs/00-executive-brief.md`: two pages, written for a CMO. No architecture jargon. The business case, the three decisions taken, the risks accepted. This artifact is the one that proves "communicate complex technical solutions to business stakeholders."

---

## 3. Repository layout

```text
Marketing-ai-workflow/
├── README.md
├── LICENSE                      # MIT — repo is public
├── .gitignore                   # Python + editor + .env
├── PROJECT_PLAN.md              # this file
├── docs/
│   ├── 00-executive-brief.md
│   ├── 01-current-state-process-map.md
│   ├── 02-bottleneck-register.md
│   ├── 03-data-landscape.md
│   ├── 04-target-architecture.md
│   ├── 05-data-pipelines.md
│   ├── 06-interface-spec.md
│   ├── 07-nfr-budgets.md
│   ├── 08-vendor-evaluation.md
│   ├── 09-platform-roadmap-ask.md
│   ├── 10-governance.md
│   └── adr/
│       └── 0001-*.md ...
├── specs/
│   ├── agent-gateway.openapi.yaml
│   └── data-contracts/
│       ├── dam-asset-feed.yaml
│       └── lifecycle-segment-feed.yaml
├── reference-slice/
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   ├── src/mawo/
│   │   ├── gateway.py           # FastAPI app
│   │   ├── providers/           # abstraction + mock + one real adapter
│   │   ├── retrieval/
│   │   ├── policy/              # governance enforcement
│   │   └── trace.py
│   ├── corpus/                  # fictional MRG documents
│   ├── bench/latency_harness.py
│   └── tests/
└── .github/workflows/ci.yml
```

**Diagrams:** Mermaid only, committed inline in the markdown. No binary image files, no external diagram tools. Mermaid renders on GitHub and stays diffable.

---

## 4. Execution sequence

Work in this order. Do not start Phase 2 until Phase 1 is complete, because the slice must implement specs that already exist — building code first and back-filling the spec produces exactly the artifact-as-decoration failure this project is meant to avoid.

**Step 1 — Scaffold.** `git init`. Repo layout, README stub, CI that lints markdown and validates the OpenAPI file. Also: `LICENSE` (MIT, since question 3 defaults to public), `.gitignore` covering Python artifacts, editor files, and `.env` — the real-provider adapter reads a key from env and nothing should make it easy to commit one. Commit.

**Step 2 — D1, D2, D3.** The assessment layer. These are the factual base every later document cites. Commit each.

**Step 3 — D4, D5, D6, D7.** The design layer. D5 and D6 must be internally consistent — the pipeline outputs feed the gateway inputs; if they disagree, the reviewer will notice.

**Step 4 — D8, D9, D10.** The judgment layer. Written last among the artifacts because they cite everything above.

**Step 5 — D11.** ADRs. Retro-write them against decisions actually taken in steps 3–4. Each ADR must name the alternative that lost and why.

**Step 6 — D12.** The runnable slice. Then run the latency harness and update D7 with `[measured]` numbers. If measured numbers violate the budgets you wrote, **do not quietly edit the budget** — add a short "budget variance" note explaining the gap. That honesty is itself a signal.

**Step 7 — D13, D14.** README and executive brief, written last because they summarize.

**Commit discipline:** one commit per deliverable, conventional-commit style, message body stating what decision the document drives. The commit history is part of what a reviewer reads.

---

## 5. Quality bar

A reviewer for this role is looking for **judgment under constraint**, not comprehensiveness. Apply these tests before considering any document done:

- **The rejection test.** Does this document say no to something? A doc where every option is viable and every AI application is recommended demonstrates nothing. D2, D8, and D11 must each contain a clear, reasoned rejection.
- **The trade-off test.** Every recommendation names what it costs. "Use RAG" is not a decision; "use RAG over fine-tuning, accepting +180ms p95 and a retrieval-quality dependency, because claims content changes weekly and fine-tune cycle time can't track it" is.
- **The audience test.** D14 must be readable by a CMO. D9 must be readable by a platform engineering director who is protective of their roadmap. If both read the same, both are wrong.
- **The provenance test.** Every number is labeled `[illustrative]` or `[measured]`. No unlabeled numbers anywhere in the repo.
- **The scope test.** Nothing in the repo claims Robin built the underlying models. The framing is consistently: assess, specify, validate, govern.

---

## 6. Explicitly out of scope

Do not build any of the following, even if they seem natural:

- A web UI, dashboard, or admin console
- Authentication, user management, or multi-tenancy implementation
- A real integration with any actual vendor SaaS product
- Model training, fine-tuning, or evaluation harnesses beyond the single policy check
- More than one runnable vertical slice
- Cloud deployment, Terraform, or Kubernetes manifests (an architecture *diagram* of the target deployment belongs in D4; the IaC does not)

---

## 7. Open questions for Robin

Flag these back rather than guessing:

1. ~~**Cloud posture.**~~ **ANSWERED (2026-07-22): AWS**, with the "Azure equivalence" table. Rationale: it is where Robin's depth actually is, so it survives live questioning. See D4's row in section 2 for what to build.
2. **Depth of the runnable slice.** Is the mock-provider default acceptable, or does he want it wired to a real Claude API key for demos? **Default: mock by default, real adapter present and documented but opt-in via env var.**
3. **Public or private repo.** Affects whether the README needs a stronger fictional-scenario disclaimer up top. **Default: assume public, write the strong disclaimer.**
4. **Should this link from the CV?** If yes, the CV's "Selected Architecture Work" section needs a fourth entry and the URL — a separate task in the `career-ops` project, not this one.

---

## 8. Definition of done

- [x] All of D1–D11 exist, each with an audience line and a "What this changes" section
- [x] D5 and D9 are the strongest documents in the repo (they carry the gap-closing load)
- [x] `reference-slice` runs clean via `docker compose up` with no API keys set *(Phase-2 dependent)* — verified: the Docker image builds cleanly (`docker compose build`), and end-to-end behavior was confirmed via a live HTTP smoke test against the app run directly (`uvicorn`) with zero API keys, since the local machine's Docker Desktop was unavailable (host-side disk issue, unrelated to this repo) at verification time. CI's `slice-tests` job independently confirms a clean install + test run on a fresh checkout.
- [x] Latency harness produces `[measured]` numbers now reflected in D7 *(Phase-2 dependent)*
- [x] Every number in the repo is labeled `[illustrative]` or `[measured]`
- [x] Fictional-scenario disclaimer present in README and in every doc header
- [x] At least three documented rejections (D2, D8, D11)
- [x] CI green: markdown lint + OpenAPI validation + slice tests *(slice tests Phase-2 dependent)* — confirmed on GitHub Actions, not just locally
- [x] `LICENSE` and `.gitignore` present; no API key committed anywhere in history
- [x] README's fifteen-minute path actually takes fifteen minutes — read it end to end and time it

Items marked *(Phase-2 dependent)* are struck if the runnable slice is cut per section 0. Everything else holds regardless. Phase 2 was not cut — D12 was built and verified.
