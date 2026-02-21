from core.config import USE_MOCK_LLM
from llm.gemini_config import generate_response


def explain_sql(sql: str):
    sql_upper = sql.upper()

    # --------------------------------------------
    # MOCK MODE (Deterministic Explanation)
    # --------------------------------------------
    if USE_MOCK_LLM:

        explanation_parts = []

        # Aggregations
        if "COUNT(" in sql_upper:
            explanation_parts.append(
                "It counts the number of matching records in the dataset."
            )

        if "SUM(" in sql_upper:
            explanation_parts.append(
                "It calculates the total aggregated value."
            )

        if "AVG(" in sql_upper:
            explanation_parts.append(
                "It calculates the average value from the selected data."
            )

        # Joins
        if "JOIN" in sql_upper:
            explanation_parts.append(
                "It combines data from multiple related tables."
            )

        # Grouping
        if "GROUP BY" in sql_upper:
            explanation_parts.append(
                "It groups the results based on specific columns."
            )

        # Sorting
        if "ORDER BY" in sql_upper:
            explanation_parts.append(
                "It sorts the results based on defined criteria."
            )

        # Limiting
        if "LIMIT" in sql_upper:
            explanation_parts.append(
                "It restricts the number of rows returned."
            )

        # Fallback
        if not explanation_parts:
            return "This query retrieves data from the database."

        return " ".join(explanation_parts)

    # --------------------------------------------
    # REAL GEMINI MODE (Portfolio-Grade Prompt)
    # --------------------------------------------
    prompt = f"""
You are a senior data analyst explaining SQL queries to business stakeholders.

Analyze the SQL carefully and explain:

1. What tables are involved
2. Whether joins are used and why
3. Any aggregation functions used (SUM, AVG, COUNT, etc.)
4. Whether grouping is applied
5. Whether sorting or limiting is applied
6. What the final result represents in business terms

Keep the explanation:
- Clear
- Professional
- Business-friendly
- Concise (4–6 sentences max)

Do NOT just describe SQL syntax.
Explain the business meaning and insight.

SQL:
{sql}

Explanation:
"""

    return generate_response(prompt)