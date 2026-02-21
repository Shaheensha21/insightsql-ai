from core.config import USE_MOCK_LLM
from llm.gemini_config import generate_response
from llm.intent_detector import detect_intent
import re


# --------------------------------------------
# CLEAN SQL OUTPUT
# --------------------------------------------
def clean_sql_output(sql: str) -> str:
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()


# --------------------------------------------
# RULE-BASED SMART GENERATOR
# --------------------------------------------
def rule_based_sql(user_query: str) -> str:
    q = user_query.lower().strip()

    # COUNT PAYMENTS
    if ("how many" in q or "count" in q) and "payment" in q:
        return "SELECT COUNT(*) AS total_payments FROM payments;"

    # COUNT ORDERS
    if ("how many" in q or "count" in q) and "order" in q:
        return "SELECT COUNT(*) AS total_orders FROM orders;"

    # AVERAGE ORDER VALUE
    if "average" in q and "order" in q:
        return "SELECT AVG(total_amount) AS avg_order_value FROM orders;"

    # TOTAL REVENUE
    if "total revenue" in q or "sum revenue" in q:
        return """
        SELECT COALESCE(SUM(amount), 0) AS total_revenue
        FROM payments
        WHERE status = 'Completed';
        """

    # TOTAL PRODUCTS
    if "total product" in q:
        return "SELECT COUNT(*) AS total_products FROM products;"

    return None


# --------------------------------------------
# MAIN GENERATOR
# --------------------------------------------
def generate_sql(user_query: str, schema: str):

    # 🔥 1️⃣ RULE-BASED OVERRIDE (FAST + ACCURATE)
    rule_sql = rule_based_sql(user_query)
    if rule_sql:
        return rule_sql

    # 🔥 2️⃣ MOCK MODE
    if USE_MOCK_LLM:
        return "SELECT * FROM orders LIMIT 5;"

    # 🔥 3️⃣ REAL LLM MODE
    intent = detect_intent(user_query)

    prompt = f"""
You are a senior PostgreSQL data analyst.

Database Schema:
{schema}

Intent Detected:
{intent}

Rules:
- Generate ONLY valid PostgreSQL SELECT queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER.
- Do NOT explain anything.
- Do NOT use markdown.
- Return only raw SQL.
- Use COUNT() for how many questions.
- Use AVG() for average questions.
- Use SUM() for total questions.
- Do NOT use SELECT * unless explicitly requested.
- Use LIMIT only when ranking (top N).

User Question:
{user_query}

SQL:
"""

    raw_sql = generate_response(prompt)
    return clean_sql_output(raw_sql)