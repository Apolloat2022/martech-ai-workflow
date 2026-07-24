"""FastAPI agent gateway - reference implementation of a subset of
specs/agent-gateway.openapi.yaml (invoke, feedback, health; /v1/stream is
cut from this slice, see reference-slice/README.md).
"""
from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException

from . import store
from .policy import engine as policy_engine
from .providers import get_provider
from .providers.base import ProviderOutput
from .retrieval.index import RetrievalIndex
from .schemas import (
    FeedbackRequest,
    HealthResponse,
    InvokeRequest,
    InvokeResponse,
    PolicyVerdict,
    TraceInfo,
    UseCase,
)
from .trace import StageTimer

CORPUS_ROOT = Path(
    os.environ.get("MAWO_CORPUS_ROOT", Path(__file__).resolve().parents[2] / "corpus")
)

_indexes: dict[str, RetrievalIndex] = {}


def build_indexes() -> None:
    """Exposed separately from the app's lifespan so bench/latency_harness.py
    can build the same indexes without running a server."""
    _indexes["claims_brand_prescreen"] = RetrievalIndex(
        [CORPUS_ROOT / "brand_guidelines", CORPUS_ROOT / "claims_specs"]
    )
    _indexes["localization_claims_check"] = RetrievalIndex(
        [CORPUS_ROOT / "market_claims_taxonomy", CORPUS_ROOT / "claims_specs"]
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    build_indexes()
    store.init_db()
    yield


app = FastAPI(title="MAWO Agent Gateway (reference slice)", lifespan=lifespan)


def _build_query(request: InvokeRequest) -> str:
    if request.use_case == UseCase.CLAIMS_BRAND_PRESCREEN:
        return request.input["creative_text"]
    market = request.input.get("market_code", "")
    return f"{market} {request.input['localized_text']}"


def _build_output(use_case: UseCase, result: ProviderOutput) -> dict:
    if use_case == UseCase.PERFORMANCE_READOUT_SYNTHESIS:
        return {"narrative": result.narrative}
    return {"flagged_phrases": result.candidate_claims}


def run_invoke(request: InvokeRequest) -> InvokeResponse:
    """Core pipeline, factored out of the route so the latency harness can
    call it directly without a running HTTP server."""
    timer = StageTimer()
    request_id = str(uuid.uuid4())
    provider = get_provider()

    with timer.stage("network_in"):
        pass  # request already parsed/validated by FastAPI+pydantic by this point

    if request.use_case == UseCase.PERFORMANCE_READOUT_SYNTHESIS:
        retrieved_ids = list(request.input["segment_ids"])
        context_chunks: list[str] = []
        with timer.stage("retrieval"):
            pass  # UC-3 reads the metrics store, not the retrieval index - see D5
        timer.mark_na("rerank")
    else:
        query = _build_query(request)
        index = _indexes[request.use_case.value]
        with timer.stage("retrieval"):
            hits = index.search(query, top_k=3)
        with timer.stage("rerank"):
            hits = index.rerank(query, hits)
        retrieved_ids = [d.doc_id for d in hits]
        context_chunks = [d.text for d in hits]

    with timer.stage("inference"):
        result = provider.generate(request.use_case.value, request.input, context_chunks)

    with timer.stage("policy_check"):
        status, reasons = policy_engine.safe_check(result.candidate_claims, context_chunks)

    with timer.stage("network_out"):
        pass

    response = InvokeResponse(
        request_id=request_id,
        use_case=request.use_case,
        retrieved_doc_ids=retrieved_ids,
        policy_verdict=PolicyVerdict(status=status, reasons=reasons),
        output=_build_output(request.use_case, result),
        trace=TraceInfo(
            stage_timings_ms=timer.timings_ms,
            model=result.model,
            model_version=result.model_version,
        ),
    )
    store.save_trace(response)
    return response


@app.post("/v1/invoke", response_model=InvokeResponse)
def invoke(request: InvokeRequest) -> InvokeResponse:
    try:
        return run_invoke(request)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"missing required input field: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/feedback", status_code=204)
def feedback(request: FeedbackRequest) -> None:
    store.save_feedback(request)


@app.get("/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    retrieval_status = "ok" if _indexes else "degraded"
    provider_status = "ok"
    overall = "ok" if retrieval_status == "ok" and provider_status == "ok" else "degraded"
    return HealthResponse(
        status=overall,
        retrieval_index_status=retrieval_status,
        model_provider_status=provider_status,
    )
