"""In-memory retrieval index - the reference-slice stand-in for D4's
Retrieval Index / OpenSearch Serverless. Rebuilt from the corpus/ directory
at startup; no persistence, matching "no standalone vector store container".
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .embeddings import cosine_similarity, vectorize


@dataclass
class Document:
    doc_id: str
    text: str
    vector: object


class RetrievalIndex:
    def __init__(self, corpus_dirs: list[Path]) -> None:
        self.documents: list[Document] = []
        for directory in corpus_dirs:
            if not directory.exists():
                continue
            for path in sorted(directory.glob("*.md")):
                text = path.read_text(encoding="utf-8")
                doc_id = f"{directory.name}/{path.stem}"
                self.documents.append(Document(doc_id, text, vectorize(text)))

    def search(self, query: str, top_k: int = 3) -> list[Document]:
        query_vec = vectorize(query)
        scored = [(cosine_similarity(query_vec, d.vector), d) for d in self.documents]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [d for score, d in scored[:top_k] if score > 0]

    def rerank(self, query: str, docs: list[Document]) -> list[Document]:
        """Small, real rerank step - not a no-op: boosts documents that
        share an exact phrase with the query beyond bag-of-words overlap
        alone. See D7 - rerank is a named stage with actual work in it for
        UC-1/UC-2, not a placeholder."""
        query_lower = query.lower()
        phrases = [p.strip() for p in query_lower.split(".") if len(p.strip()) > 8]

        def score(doc: Document) -> int:
            lower = doc.text.lower()
            return sum(1 for phrase in phrases if phrase in lower)

        return sorted(docs, key=score, reverse=True)
