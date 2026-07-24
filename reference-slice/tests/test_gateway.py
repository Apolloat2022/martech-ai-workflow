import os

os.environ["MAWO_DB_PATH"] = ":memory:"
os.environ.pop("ANTHROPIC_API_KEY", None)  # force the mock provider for deterministic tests

from fastapi.testclient import TestClient  # noqa: E402

from mawo import store  # noqa: E402
from mawo.gateway import app, build_indexes  # noqa: E402

# Built explicitly rather than relying on the app's lifespan handler, which
# only runs under TestClient's context-manager form.
build_indexes()
store.init_db()

client = TestClient(app)


def test_health():
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_invoke_claims_brand_prescreen_substantiated_product_is_clear():
    resp = client.post(
        "/v1/invoke",
        json={
            "use_case": "claims_brand_prescreen",
            "submitted_by": "test",
            "input": {
                "creative_text": "Glow Serum X1 is clinically tested for better hydration.",
                "brief_id": "BR-1",
                "product_ids": ["GS-X1-30ML"],
            },
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["policy_verdict"]["status"] == "clear"
    assert any("claims_specs/glow-serum-x1" in doc_id for doc_id in body["retrieved_doc_ids"])
    assert set(body["trace"]["stage_timings_ms"]) == {
        "network_in", "retrieval", "rerank", "inference", "policy_check", "network_out",
    }


def test_invoke_claims_brand_prescreen_unsubstantiated_product_is_flagged():
    resp = client.post(
        "/v1/invoke",
        json={
            "use_case": "claims_brand_prescreen",
            "submitted_by": "test",
            "input": {
                "creative_text": "Hydra Boost Cream is clinically proven to guarantee results.",
                "brief_id": "BR-2",
                "product_ids": ["HBC-50ML"],
            },
        },
    )
    assert resp.status_code == 200
    assert resp.json()["policy_verdict"]["status"] == "flagged_for_review"


def test_invoke_localization_claims_check():
    resp = client.post(
        "/v1/invoke",
        json={
            "use_case": "localization_claims_check",
            "submitted_by": "test",
            "input": {
                "localized_text": "Notre produit est clinically proven.",
                "source_text": "Our product is clinically tested.",
                "market_code": "EU",
                "brief_id": "BR-3",
            },
        },
    )
    assert resp.status_code == 200
    assert resp.json()["use_case"] == "localization_claims_check"


def test_invoke_performance_readout_synthesis():
    resp = client.post(
        "/v1/invoke",
        json={
            "use_case": "performance_readout_synthesis",
            "submitted_by": "test",
            "input": {"cycle_id": "C-1", "segment_ids": ["seg-a", "seg-b"]},
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["retrieved_doc_ids"] == ["seg-a", "seg-b"]
    assert body["trace"]["stage_timings_ms"]["rerank"] == 0.0
    assert "narrative" in body["output"]


def test_invoke_missing_field_is_400():
    resp = client.post(
        "/v1/invoke",
        json={
            "use_case": "claims_brand_prescreen",
            "submitted_by": "test",
            "input": {"brief_id": "BR-4"},
        },
    )
    assert resp.status_code == 400


def test_feedback_accepts_and_returns_204():
    resp = client.post(
        "/v1/feedback",
        json={
            "request_id": "11111111-1111-1111-1111-111111111111",
            "verdict_outcome": "upheld",
            "reviewer_id": "reviewer-1",
            "notes": "agreed with the flag",
        },
    )
    assert resp.status_code == 204
