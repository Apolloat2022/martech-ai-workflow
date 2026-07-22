# To-Be AI Architecture

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Platform engineering, solution architects, security/governance reviewers.

## Which use cases this architecture serves

[D2](02-bottleneck-register.md) scored seven handoffs High or Medium for automation candidacy. Three become AI use cases here; the other four are deterministic fixes with no model in the loop, designed in [D5](05-data-pipelines.md) instead:

| Use case | Closes | Nature |
|---|---|---|
| **UC-1 — Claims & Brand Pre-Screen Assistant** | B-01, B-03 | Interactive retrieval-augmented check of in-flight creative against brand guidelines and claims-relevant product specs, run during drafting and again before submission |
| **UC-2 — Localization Claims Consistency Checker** | B-02 | Per-market check of localized copy for claims-bearing phrases and back-translation drift against a legal-owned claims taxonomy |
| **UC-3 — Performance Readout Synthesis** | B-07 | Narrative summary generated from pre-aggregated, non-PII lifecycle and analytics rollups |

B-04 (brief intake), B-05 (DAM metadata), and B-06 (activation scheduling) are not AI use cases — a structured form, a metadata template, and a shared calendar solve them respectively. Building a model into a form-validation problem would be over-applying the technology exactly where D2 already flagged the simpler fix as sufficient.

## System context (C4 L1)

```mermaid
C4Context
  title System Context - MRG Marketing AI Platform

  Person(agencyUser, "Agency Creative", "Drafts campaign creative")
  Person(brandUser, "Brand Reviewer", "Reviews creative for brand fit")
  Person(legalUser, "Legal & Compliance Reviewer", "Reviews claims substantiation, owns the claims taxonomy")
  Person(pmmUser, "Product Marketing Manager", "Owns the brief and the performance readout")

  System(gateway, "MRG Marketing AI Platform", "Agent Gateway: retrieval + policy-check assistants for UC-1, UC-2, UC-3")

  System_Ext(cms, "CMS (S1)", "Brand guideline content")
  System_Ext(dam, "DAM (S2)", "Creative assets & claims tags")
  System_Ext(pim, "PIM (S5)", "Product specs & claims data")
  System_Ext(ticketing, "Ticketing (S7)", "Brief content")
  System_Ext(crmCdp, "CRM / CDP (S3, S4)", "Lifecycle segments - aggregated only")
  System_Ext(modelProvider, "Third-Party Model Provider", "Managed inference")

  Rel(agencyUser, gateway, "Submits creative for pre-screen (UC-1)")
  Rel(brandUser, gateway, "Reviews flagged items")
  Rel(legalUser, gateway, "Reviews flagged items; owns the claims taxonomy input to UC-2")
  Rel(pmmUser, gateway, "Requests performance readout (UC-3)")

  Rel(gateway, cms, "Reads brand guideline docs")
  Rel(gateway, dam, "Reads asset metadata & claims tags")
  Rel(gateway, pim, "Reads product claims specs")
  Rel(gateway, ticketing, "Reads brief content")
  Rel(gateway, crmCdp, "Reads the aggregated segment feed only - see D5 data contract")
  Rel(gateway, modelProvider, "Sends de-identified prompt context for inference")
```

## Container view (C4 L2)

```mermaid
C4Container
  title Container View - MRG Marketing AI Platform (Agent Gateway)

  Person(callers, "Internal callers", "Agency, Brand, Legal, PMM tooling")

  System_Boundary(platform, "MRG Marketing AI Platform") {
    Container(gateway, "Agent Gateway", "FastAPI service", "invoke / stream / feedback / health - see D6")
    Container(policy, "Policy Engine", "Rule engine", "Enforces D10 governance rules; fails closed, never open")
    Container(retrieval, "Retrieval Service", "Vector search", "Queries the retrieval index for UC-1/UC-2")
    Container(ingestion, "Ingestion Workers", "Pipeline jobs", "Populate the index and metrics store per D5's contracts")
    ContainerDb(index, "Retrieval Index", "Vector store", "Chunked/embedded CMS + DAM + PIM + brief content - no PII")
    ContainerDb(metrics, "Metrics Store", "Aggregated store", "Lifecycle segment feed + analytics rollups, for UC-3")
    Container(trace, "Trace Store", "Structured logs", "Per-request stage timings, model/version, policy verdict")
  }

  System_Ext(modelProvider, "Third-Party Model Provider", "Managed inference")
  System_Ext(sources, "Source systems", "CMS, DAM, PIM, Ticketing, CRM/CDP")

  Rel(callers, gateway, "invoke / stream / feedback")
  Rel(gateway, retrieval, "Retrieves context for UC-1/UC-2")
  Rel(retrieval, index, "Vector search")
  Rel(gateway, metrics, "Reads aggregates for UC-3")
  Rel(ingestion, sources, "Pulls per D5 ingestion paths")
  Rel(ingestion, index, "Writes chunks/embeddings")
  Rel(ingestion, metrics, "Writes aggregated feed")
  Rel(gateway, modelProvider, "Sends prompt context - crosses trust boundary")
  Rel(gateway, policy, "Runs policy check before returning any response")
  Rel(gateway, trace, "Writes structured trace")
```

## Data flow and trust boundaries

```mermaid
flowchart LR
    subgraph TB1["Trust Boundary 1 - MRG Corporate Network"]
        U["Human callers<br/>(Agency, Brand, Legal, PMM)"]
    end

    subgraph TB2["Trust Boundary 2 - MRG Cloud Account (Agent Gateway)"]
        GW["Agent Gateway"]
        POL["Policy Engine<br/>(fails closed)"]
        RET["Retrieval Service"]
        IDX[("Retrieval Index<br/>No PII - S1/S2/S5/S7 only")]
        MET[("Metrics Store<br/>Aggregated only, count >= 50<br/>lifecycle-segment-feed contract")]
    end

    subgraph TB3["Trust Boundary 3 - Third-Party Model Provider<br/>(data leaves MRG's environment)"]
        MODEL["Managed inference API"]
    end

    U -->|request| GW
    GW --> RET
    RET --> IDX
    GW --> MET
    GW -->|de-identified prompt context only| MODEL
    MODEL -->|completion| GW
    GW --> POL
    POL -->|verdict| GW
    GW -->|response| U
```

The only PII-relevant crossing in the whole diagram is TB2 → TB3, and by contract nothing that crosses it originates from a PII-flagged source: the retrieval index is built exclusively from S1/S2/S5/S7 (all PII: No or Low per [D3](03-data-landscape.md)), and the metrics store only ever holds aggregates suppressed below a 50-member floor (see D5's `lifecycle-segment-feed` contract). S3 and S4, the two PII-flagged systems, never appear inside TB2 in row-level form — they are pre-aggregated before this boundary, not inside it.

## Deployment view (AWS)

**Cloud posture: AWS.** Not because it's materially better suited to this workload than Azure — it isn't — but because it's where the author's depth actually is, and a deployment diagram that can't survive a follow-up question is worse than none. The Azure equivalence table below exists so "we're a Microsoft shop" costs one paragraph, not a redesign.

```mermaid
flowchart TB
    subgraph VPC["AWS Account - VPC (single region, matching DAM/PIM primary regions)"]
        subgraph PRIV["Private subnets"]
            FARGATE["ECS Fargate<br/>Agent Gateway + Policy Engine + Retrieval Service"]
            OS[("OpenSearch Serverless<br/>Retrieval Index")]
        end
        SM["Secrets Manager<br/>(API keys, model provider credentials)"]
        EB["EventBridge<br/>(DAM/CMS publish-webhook triggers)"]
    end
    S3B[("S3<br/>Corpus staging + Metrics Store")]
    BR["Bedrock<br/>(managed inference, same region)"]
    CW["CloudWatch + X-Ray<br/>(observability, feeds Trace Store)"]

    EB --> FARGATE
    FARGATE --> OS
    FARGATE --> S3B
    FARGATE --> SM
    FARGATE -->|inference call - crosses TB3| BR
    FARGATE --> CW
```

This is the same TB1/TB2/TB3 structure as the trust-boundary diagram above: the VPC is TB2, Bedrock is TB3, and the crossing is the same single edge.

### Azure equivalence

| Concern | AWS (as drawn) | Azure equivalent | Notes / where the mapping frays |
|---|---|---|---|
| Compute (gateway) | ECS Fargate | Container Apps | Near-equivalent |
| Managed inference | Bedrock | Azure OpenAI / AI Foundry | Model catalogues differ — this is the real switching cost, not the compute |
| Vector / retrieval | OpenSearch Serverless | AI Search | Hybrid-search semantics differ |
| Object storage | S3 | Blob Storage | Equivalent |
| Secrets | Secrets Manager | Key Vault | Equivalent |
| Eventing | EventBridge | Event Grid | Equivalent in shape, different operational model |
| Observability | CloudWatch + X-Ray | Monitor + App Insights | Equivalent |

The managed-inference row is the one that matters: model catalogue differences, not infrastructure, are what make an AWS-to-Azure move expensive here. That's the same lock-in argument [D8](08-vendor-evaluation.md) makes independently about vendor choice — this table is the infrastructure-level version of it.

## What this changes

D5's ingestion paths and data contracts are scoped to feed exactly the two stores drawn here (the retrieval index and the metrics store) — nothing else. D6's API surface is the only sanctioned way to reach the Policy Engine or Retrieval Service; no consumer talks to the index or metrics store directly. D7's NFR budgets are per-use-case latency budgets for calls that cross this exact diagram, stage for stage. If a future change adds a fourth use case or a new source system, it has to be placed on this diagram — including which trust boundary it sits inside — before D5-D7 are updated to match.
