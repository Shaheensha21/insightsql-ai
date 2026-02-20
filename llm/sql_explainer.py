from core.config import USE_MOCK_LLM
from llm.gemini_config import generate_response

def explain_sql(sql: str):
    sql_upper = sql.upper()

    if USE_MOCK_LLM:

        # Special Case: Average Revenue Per Customer
        if "AVG(" in sql_upper and "GROUP BY" in sql_upper and "CUSTOMER" in sql_upper:
            return (
                "This query first calculates the total completed revenue for each customer "
                "and then computes the average revenue generated per customer across the dataset."
            )

        explanation_parts = []

        if "AVG(" in sql_upper:
            explanation_parts.append("It calculates an average value.")
        if "SUM(" in sql_upper:
            explanation_parts.append("It calculates a total sum.")
        if "COUNT(" in sql_upper:
            explanation_parts.append("It counts the number of records.")
        if "JOIN" in sql_upper:
            explanation_parts.append("It combines data from multiple related tables.")
        if "GROUP BY" in sql_upper:
            explanation_parts.append("It groups the results based on specific columns.")
        if "ORDER BY" in sql_upper:
            explanation_parts.append("It sorts the results.")
        if "LIMIT" in sql_upper:
            explanation_parts.append("It limits the number of rows returned.")

        if not explanation_parts:
            return "This query retrieves data from the database."

        return " ".join(explanation_parts)



    # 🔥 REAL GEMINI MODE (Portfolio-Grade Prompt)

    prompt = f"""
You are a senior data analyst explaining SQL queries to business stakeholders.

Analyze the SQL carefully and explain:

1. What tables are involved
2. Whether joins are used and why
3. Any aggregation functions used (SUM, AVG, COUNT, etc.)
4. Whether grouping is applied
5. Whether sorting or limiting is applied
6. What the final result represents in business terms

Keep the explanation clear, professional, and business-friendly.
Do NOT just describe SQL syntax — explain the business meaning.

SQL:
{sql}

Explanation:
"""

    return generate_response(prompt)
