from typing import Any

from app.services.rag_service import rag_service


KNOWLEDGE_DOCUMENTS = rag_service.documents


def search_knowledge(
    query: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    return rag_service.search(
        query=query,
        limit=limit,
    )