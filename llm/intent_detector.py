def detect_intent(user_query: str) -> str:
    q = user_query.lower()

    if "how many" in q or "count" in q:
        return "COUNT"

    if "average" in q or "avg" in q:
        return "AVERAGE"

    if "total" in q or "sum" in q:
        return "SUM"

    if "top" in q or "highest" in q or "best" in q:
        return "RANKING"

    if "trend" in q or "over time" in q:
        return "TIME_SERIES"

    return "GENERAL_QUERY"