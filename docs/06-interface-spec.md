# Interface & Integration Spec

> Fictional reference scenario authored as an architecture portfolio piece. Not a record of a client engagement.

**Audience:** Engineering teams integrating with the agent gateway.

Companion file: [`specs/agent-gateway.openapi.yaml`](../specs/agent-gateway.openapi.yaml) (OpenAPI 3.1). This document covers what the schema alone doesn't: auth, idempotency, error taxonomy, versioning, and tenancy.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/invoke` | POST | Single-shot request for any of UC-1, UC-2, UC-3. Returns retrieved doc IDs, policy verdict, and output in one response |
| `/v1/stream` | POST | Streaming variant of `invoke`, Server-Sent Events, for UC-1's interactive drafting use |
| `/v1/feedback` | POST | Human reviewer records agree/override on a policy verdict, closing the loop for [D10](10-governance.md)'s calibration needs |
| `/v1/health` | GET | Liveness/readiness, reports retrieval-index and model-provider status separately |

`invoke`'s response shape matches [D5](05-data-pipelines.md) directly: `retrieved_doc_ids` are `asset_id` values from the `dam-asset-feed` contract, and UC-3 requests are only accepted with fields the `lifecycle-segment-feed` contract actually produces. This is not a coincidence — the two documents were written to agree, and a future change to either has to keep them agreeing.

## Auth model

Service-to-service API key, issued per consuming system (the ticketing/brief system, the DAM, etc.), presented via an `Authorization: Bearer` header. There is no user-level authentication at the gateway: which human submitted a request is passed as a claim in the request body (`submitted_by`), asserted by the calling system, not verified by the gateway. That's a deliberate boundary, not an oversight — building a second identity system to re-verify what the calling system (which already has its own SSO-backed identity) already knows would duplicate build-side work this role is explicitly not meant to do (see [PROJECT_PLAN.md](../PROJECT_PLAN.md) section 0). A production deployment sits behind MRG's existing internal-network boundary; the API key controls which *systems* can call the gateway, not which *people*.

## Idempotency

`invoke`, `stream`, and `feedback` all require an `Idempotency-Key` header (client-generated UUID). The gateway caches the full response for 24 hours keyed on `(idempotency_key, use_case)` and returns the cached response on a retried call rather than re-running inference — necessary because UC-1/UC-2 calls are not free, and a naive retry-on-timeout client would otherwise double-charge every transient network blip against the model provider. `stream` needs this at least as much as `invoke`: a dropped SSE connection is a more common retry trigger than a dropped single-shot request.

## Error taxonomy

All errors return a structured body: `{"error": {"code", "message", "request_id", "retriable"}}`.

| Code | HTTP status | Retriable | Meaning |
|---|---|---|---|
| `validation_error` | 400 | No | Request body fails schema validation |
| `unsupported_use_case` | 400 | No | `use_case` value isn't one of UC-1/UC-2/UC-3 |
| `unauthorized` | 401 | No | Missing or invalid API key |
| `rate_limited` | 429 | Yes (with backoff) | Caller exceeded its rate allocation |
| `retrieval_unavailable` | 503 | Yes | Retrieval index degraded — see D7's degradation ladder |
| `upstream_provider_error` | 502 | Yes | Model provider call failed |
| `policy_engine_error` | 503 | **No** | Policy engine is unreachable. Not retriable, because per D7's degradation ladder the gateway fails closed here — routing to human review rather than retrying toward an auto-clear |
| `internal_error` | 500 | Yes | Unclassified gateway fault |

`policy_engine_error` is deliberately the one non-retriable 5xx: a client that retries past a policy-engine outage hoping for a clean auto-clear is exactly the failure mode D2's B-10 row exists to prevent.

## Versioning policy

URI versioning (`/v1/...`). Additive, backward-compatible changes (new optional field, new enum value) ship without a version bump. Breaking changes ship as `/v2` with the same discipline as D5's data contracts: 30 days' notice, 60-day deprecation window for the prior version. Keeping the two versioning policies identical is deliberate — a data engineer and an API consumer should be able to learn one deprecation rhythm and apply it across the whole platform.

## Tenancy

Single-tenant. Multi-tenancy is explicitly out of scope (see [PROJECT_PLAN.md](../PROJECT_PLAN.md) section 6) and is not designed for speculatively — no reserved-but-unused `tenant_id` field, no placeholder isolation layer. If MRG ever needs a second tenant, that is a new major version built when the requirement is real, not a field carried unused from day one on the chance it might be needed.

## What this changes

This is the contract engineering teams build the gateway against, and the contract [D7](07-nfr-budgets.md)'s latency budgets are measured per-call against. A change to `invoke`'s request or response shape that isn't reflected in the OpenAPI file first is not a valid change — the markdown and the YAML are meant to be read together, and if they disagree, the YAML is authoritative for the wire format and this document is authoritative for the operational policy around it.
