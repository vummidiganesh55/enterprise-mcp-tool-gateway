from app.tools.knowledge.search import (
    search_knowledge,
)

from app.tools.knowledge.retrieve import (
    retrieve_document,
)


def test_knowledge_search():

    results = search_knowledge(
        "customer support"
    )

    assert len(results) > 0

    assert (
        results[0]["document_id"]
        == "DOC001"
    )


def test_knowledge_search_limit():

    results = search_knowledge(
        "policy",
        limit=2,
    )

    assert len(results) <= 2


def test_retrieve_document():

    result = retrieve_document(
        "DOC002"
    )

    assert result["success"] is True
    assert (
        result["data"]["title"]
        == "Refund Policy"
    )


def test_retrieve_unknown_document():

    result = retrieve_document(
        "UNKNOWN"
    )

    assert result["success"] is False
    assert (
        result["error"]
        == "DOCUMENT_NOT_FOUND"
    )