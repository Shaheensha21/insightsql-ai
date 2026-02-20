from llm.gemini_config import generate_response


def needs_clarification(user_query: str) -> bool:
    """
    Only ask clarification if ranking words exist
    AND no metric is specified.
    """

    ranking_words = ["top", "best", "highest", "lowest", "most", "least"]

    metric_words = [
        "profit",
        "revenue",
        "sales",
        "amount",
        "quantity",
        "count",
        "sum",
        "average",
        "avg",
        "total"
    ]

    query_lower = user_query.lower()

    has_ranking = any(word in query_lower for word in ranking_words)
    has_metric = any(word in query_lower for word in metric_words)

    return has_ranking and not has_metric


def ask_clarification(user_query: str) -> str:
    """
    Use Gemini to generate a clarification question.
    """

    prompt = f"""
The user asked: "{user_query}"

This question is ambiguous.

Ask one short clarification question.
Do NOT explain anything.
Only return the question.
"""

    return generate_response(prompt).strip()
