from pathlib import Path

from mawo.retrieval.embeddings import cosine_similarity, vectorize
from mawo.retrieval.index import RetrievalIndex

CORPUS_ROOT = Path(__file__).resolve().parents[1] / "corpus"


def test_cosine_similarity_identical_text_is_one():
    vec = vectorize("clinically tested serum")
    assert abs(cosine_similarity(vec, vec) - 1.0) < 1e-9


def test_cosine_similarity_disjoint_text_is_zero():
    assert cosine_similarity(vectorize("hello world"), vectorize("xyz abc")) == 0.0


def test_index_finds_relevant_claims_spec():
    index = RetrievalIndex([CORPUS_ROOT / "claims_specs"])
    hits = index.search("is glow serum x1 clinically tested", top_k=1)
    assert hits
    assert "glow-serum-x1" in hits[0].doc_id


def test_index_returns_nothing_below_zero_similarity():
    index = RetrievalIndex([CORPUS_ROOT / "claims_specs"])
    assert index.search("zzz qqq nonexistent_token_xyz", top_k=3) == []
