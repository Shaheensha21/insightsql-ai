from core.config import USE_MOCK_LLM
from llm.gemini_config import generate_response
import re


# --------------------------------------------
# CLEAN SQL OUTPUT
# --------------------------------------------
def clean_sql_output(sql: str) -> str:
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()


# --------------------------------------------
# SMART MOCK GENERATOR
# --------------------------------------------
def mock_generate_sql(user_query: str) -> str:
    q = user_query.lower().strip()

    # TOP PRODUCT BY PROFIT
    if "top product" in q and "profit" in q:
        return """
        SELECT p.name,
               SUM(oi.quantity * (oi.unit_price - p.cost_price)) AS profit
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.name
        ORDER BY profit DESC
        LIMIT 1;
        """

    # TOP PRODUCTS BY REVENUE
    if "top" in q and "revenue" in q:
        return """
        SELECT p.name,
               SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 5;
        """

    # TOTAL REVENUE
    if "total revenue" in q:
        return """
        SELECT COALESCE(SUM(amount), 0) AS total_revenue
        FROM payments
        WHERE status = 'Completed';
        """

    # TOTAL ORDERS
    if "total orders" in q:
        return "SELECT COUNT(*) AS total_orders FROM orders;"

    # AVERAGE REVENUE PER CUSTOMER
    if "average revenue per customer" in q:
        return """
        SELECT AVG(customer_total.total_revenue) AS avg_revenue_per_customer
        FROM (
            SELECT o.customer_id,
                   SUM(p.amount) AS total_revenue
            FROM orders o
            JOIN payments p ON p.order_id = o.id
            WHERE p.status = 'Completed'
            GROUP BY o.customer_id
        ) customer_total;
        """

    # DEFAULT SAFE FALLBACK
    return "SELECT * FROM orders LIMIT 5;"


# --------------------------------------------
# MAIN GENERATOR
# --------------------------------------------
def generate_sql(user_query: str, schema: str):

    # 🔥 USE MOCK IF ENABLED
    if USE_MOCK_LLM:
        return mock_generate_sql(user_query)

    # 🔥 REAL GEMINI MODE
    prompt = f"""
You are a senior PostgreSQL data analyst.

Database Schema:
{schema}

Relationships:
- orders.customer_id → customers.id
- payments.order_id → orders.id
- order_items.order_id → orders.id
- order_items.product_id → products.id

Rules:
- Generate ONLY valid PostgreSQL SELECT queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER.
- Do NOT explain anything.
- Do NOT use markdown.
- Return only raw SQL.
- Use proper JOINs when required.
- Always use LIMIT when returning ranked results.

User Question:
{user_query}

SQL:
"""

    raw_sql = generate_response(prompt)

    return clean_sql_output(raw_sql)
