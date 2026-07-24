"""Deterministic bag-of-words vectorization and cosine similarity.

No ML library, no embedding API call - see PROJECT_PLAN.md's "no
standalone vector store container" decision and D5's chunking/embedding
strategy. This is intentionally simple: the corpus is a dozen documents,
not a production-scale index.
"""
from __future__ import annotations

import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def vectorize(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    norm_a = sum(v * v for v in a.values()) ** 0.5
    norm_b = sum(v * v for v in b.values()) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
