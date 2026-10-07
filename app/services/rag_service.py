from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.tools.knowledge.documents import KNOWLEDGE_DOCUMENTS


class RAGService:
    def __init__(self) -> None:
        self.documents = KNOWLEDGE_DOCUMENTS

        self._texts = [
            f"{document['title']} {document['content']}"
            for document in self.documents
        ]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
        )

        self.document_vectors = self.vectorizer.fit_transform(
            self._texts
        )

    def search(
        self,
        query: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.document_vectors,
        )[0]

        ranked_indices = similarities.argsort()[::-1]

        results = []

        for index in ranked_indices[:limit]:
            score = float(similarities[index])

            if score <= 0:
                continue

            document = self.documents[index]

            results.append(
                {
                    "document_id": document["document_id"],
                    "title": document["title"],
                    "content": document["content"],
                    "score": round(score, 4),
                }
            )

        return results


rag_service = RAGService()