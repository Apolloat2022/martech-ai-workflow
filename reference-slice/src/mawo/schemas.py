"""Pydantic models mirroring specs/agent-gateway.openapi.yaml.

Only the invoke/feedback/health surface is implemented here - see
reference-slice/README.md for the documented scope cut on /v1/stream.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class UseCase(str, Enum):
    CLAIMS_BRAND_PRESCREEN = "claims_brand_prescreen"
    LOCALIZATION_CLAIMS_CHECK = "localization_claims_check"
    PERFORMANCE_READOUT_SYNTHESIS = "performance_readout_synthesis"


class ClaimsBrandPrescreenInput(BaseModel):
    creative_text: str
    brief_id: str
    product_ids: list[str] = Field(default_factory=list)


class LocalizationClaimsCheckInput(BaseModel):
    localized_text: str
    source_text: str
    market_code: str
    brief_id: str


class PerformanceReadoutSynthesisInput(BaseModel):
    cycle_id: str
    segment_ids: list[str]


class InvokeRequest(BaseModel):
    use_case: UseCase
    submitted_by: str
    input: dict[str, Any]


class PolicyVerdict(BaseModel):
    status: Literal["clear", "flagged_for_review", "blocked"]
    reasons: list[str]


class TraceInfo(BaseModel):
    stage_timings_ms: dict[str, float]
    model: str
    model_version: str


class InvokeResponse(BaseModel):
    request_id: str
    use_case: UseCase
    retrieved_doc_ids: list[str]
    policy_verdict: PolicyVerdict
    output: dict[str, Any]
    trace: TraceInfo


class FeedbackRequest(BaseModel):
    request_id: str
    verdict_outcome: Literal["upheld", "overridden"]
    reviewer_id: str
    notes: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded", "down"]
    retrieval_index_status: Literal["ok", "degraded", "down"]
    model_provider_status: Literal["ok", "degraded", "down"]
