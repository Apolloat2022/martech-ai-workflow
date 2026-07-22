# Data Landscape Assessment

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Data engineering, platform engineering, marketing operations, and Legal & Compliance (for the PII and residency columns specifically).

## Scope

Eight systems touch the campaign content lifecycle mapped in [D1](01-current-state-process-map.md). This inventory is the input [D5](05-data-pipelines.md)'s pipeline design and [D6](06-interface-spec.md)'s interface spec are built against: what can feed a shared retrieval layer, what can't without a redesign, and where a trust boundary in [D4](04-target-architecture.md) has to sit.

## At a glance

| ID | System | Owner | PII flag | Integration surface | Residency |
|---|---|---|---|---|---|
| S1 | CMS (web content) | Product Marketing (Digital) | No | API (REST) | Single instance, EU (Ireland) |
| S2 | DAM (asset management) | Brand | No (rare talent/model-release metadata) | API + publish webhook | Single instance, US |
| S3 | CRM / Lifecycle platform | Lifecycle/CRM | **Yes** | API + nightly batch export | Regional instances: EU, US, APAC |
| S4 | CDP (customer data platform) | Lifecycle/CRM + Analytics (shared) | **Yes** | Streaming API + batch | Single instance, logically partitioned EU/US |
| S5 | PIM (product information) | Product Marketing (merchandising liaison) | No | API + nightly flat-file export | Single instance, US |
| S6 | Analytics platform | Analytics (within Product Marketing) | Low (pseudonymized IDs) | API (reporting) + scheduled export | Single instance, EU |
| S7 | Ticketing / workflow system | Marketing Operations (shared) | Low (internal reviewer identities only) | API (webhooks), used inconsistently | Single instance, US |
| S8 | Agency file share | Creative Agency (external); MRG has read access | Rare (occasional talent contracts) | **None** — SFTP / manual folder share | Third-party vendor, US; outside MRG's governance perimeter |

## System detail

### S1 — CMS (web content)

- **Data classes:** web page content, campaign landing pages, structured content blocks.
- **Quality issues:** inconsistent content tagging/taxonomy across regional microsites — no shared content model.
- **Refresh cadence:** real-time on publish.

### S2 — DAM (Digital Asset Management)

- **Data classes:** creative assets (images, video, layered source files), rights/usage metadata, brand claims tags.
- **Quality issues:** metadata inconsistently applied at ingestion — see [D2](02-bottleneck-register.md) B-05; duplicate assets across the four localization markets with no canonical-source link back to the master.
- **Refresh cadence:** event-driven, on ingestion.

### S3 — CRM / Lifecycle platform

- **Data classes:** customer profile, email engagement history, lifecycle segment membership.
- **Quality issues:** segment definitions drift from the CDP source of truth over time; duplicate customer records persist across the three regional instances.
- **Refresh cadence:** near-real-time for triggered sends, daily batch for segment sync.
- **Residency note:** the EU/US/APAC split exists for privacy-regulation reasons, not technical convenience — any pipeline that unifies this data has to preserve that separation, not flatten it. This is the constraint that most directly shapes D5's contract for the lifecycle-segment feed.

### S4 — CDP (Customer Data Platform)

- **Data classes:** unified customer identity graph, behavioral events, consent state.
- **Quality issues:** identity resolution gaps across channels (guest checkout, in-store purchase) undercount the actually-consented, reachable audience — a data-quality issue with a direct business cost, not just a technical one.
- **Refresh cadence:** near-real-time.
- **PII note:** consent state itself is the highest-sensitivity field in the entire landscape — any AI use case touching lifecycle/CRM segments must read consent state before, not after, retrieval. This is the anchor fact behind D10's DPIA-lite for the lifecycle/CRM use case.

### S5 — PIM (Product Information Management)

- **Data classes:** product attributes, list pricing (not customer pricing), claims-relevant product specs (ingredients, certifications, regulatory markings).
- **Quality issues:** attribute completeness varies by category; claims-relevant fields (e.g. "organic certified") are not reliably populated at product launch, which is a direct contributor to the claims-review rework loop in D2 (B-01) — legal has no reliable source to substantiate against.
- **Refresh cadence:** daily batch.

### S6 — Analytics platform (web/campaign)

- **Data classes:** campaign performance metrics, web behavioral events (aggregated, pseudonymized at this layer).
- **Quality issues:** attribution model differs from the CDP's, which is the direct cause of the manual reconciliation effort in [D2](02-bottleneck-register.md) B-07.
- **Refresh cadence:** daily.
- **PII note:** pseudonymized within this system, but joinable to identifying data via the CDP if combined carelessly — flagged Low here, not No, because the risk is in combination, not in isolation.

### S7 — Ticketing / workflow system

- **Data classes:** brief content, review status, approval history, SLA timestamps.
- **Quality issues:** brief fields are free text rather than structured — the direct cause of D2's B-04; no shared instance between the brand-review and legal-review stages, so a new ticket is created at each handoff instead of one ticket carrying state forward.
- **Refresh cadence:** real-time.

### S8 — Agency file share

- **Data classes:** creative work-in-progress files, project briefs shared externally with the agency.
- **Quality issues:** no version control — filename-based versioning is the direct cause of wrong-version submissions feeding D2's B-03 rework loop.
- **Integration surface:** none. This is the one system in the landscape with no API, webhook, or structured export of any kind — everything in and out is a manual upload or download.
- **Governance note:** this is the only system in the inventory that sits fully outside MRG's data governance perimeter, on a third-party vendor's infrastructure, with no contractual data-processing visibility beyond basic file storage. It is the clearest single candidate in this repo for a platform gap — see [D9](09-platform-roadmap-ask.md) — and it is explicitly *not* proposed as a pipeline source in D5, because ingesting from an unmanaged, unversioned, no-API file share would mean building a pipeline whose input contract nobody owns.

## What this changes

Every PII flag and residency note here is a hard constraint on [D4](04-target-architecture.md)'s trust-boundary diagram and on which two feeds D5 selects for its data-contract spec — a system flagged **Yes** for PII (S3, S4) cannot be treated the same way in pipeline design as one flagged **No** (S1, S2, S5), regardless of how convenient a unified ingestion path would be. S8's complete lack of integration surface is the reason it is excluded from D5 rather than quietly assumed away, and is the seed of one of D9's platform-gap asks.
