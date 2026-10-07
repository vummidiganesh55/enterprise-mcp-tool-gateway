from typing import Any

from app.tools.knowledge.documents import KNOWLEDGE_DOCUMENTS


def retrieve_document(
    document_id: str,
) -> dict[str, Any]:

    for document in KNOWLEDGE_DOCUMENTS:

        if document["document_id"] == document_id:
            return {
                "success": True,
                "data": document,
                "error": None,
            }

    return {
        "success": False,
        "data": None,
        "error": "DOCUMENT_NOT_FOUND",
    }