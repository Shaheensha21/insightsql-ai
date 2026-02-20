from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time
import logging

# LLM function-based modules
from llm.clarification_engine import needs_clarification, ask_clarification
from llm.sql_generator import generate_sql
from llm.sql_explainer import explain_sql

# Core modules
from core.sql_validator import SQLValidator
from core.executor import SQLExecutor

# You likely already have schema loader somewhere
from database.schema import get_schema  # If you don't have this, see note below


router = APIRouter()
logger = logging.getLogger(__name__)

validator = SQLValidator()
executor = SQLExecutor()


# ===============================
# Request / Response Models
# ===============================

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    sql: Optional[str] = None
    result: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[str] = None
    clarification: Optional[str] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    row_count: Optional[int] = None


# ===============================
# MAIN QUERY ENDPOINT
# ===============================

@router.post("/query", response_model=QueryResponse)
def handle_query(request: QueryRequest):

    request_id = str(time.time())
    logger.info(f"[{request_id}] Incoming question: {request.question}")

    try:
        start_time = time.time()

        # ===============================
        # Step 1: Clarification Check
        # ===============================

        if needs_clarification(request.question):
            clarification_question = ask_clarification(request.question)
            return QueryResponse(clarification=clarification_question)

        # ===============================
        # Step 2: Generate SQL
        # ===============================

        schema = get_schema()  # Must return schema string
        sql = generate_sql(request.question, schema)

        if not sql:
            return QueryResponse(error="Failed to generate SQL.")

        logger.info(f"[{request_id}] Generated SQL: {sql}")

        # ===============================
        # Step 3: Validate SQL
        # ===============================

        is_valid, validation_error = validator.validate(sql)

        if not is_valid:
            return QueryResponse(
                sql=sql,
                error=f"SQL Validation Failed: {validation_error}"
            )

        # ===============================
        # Step 4: Execute SQL
        # ===============================

        df = executor.execute(sql)

        execution_time = round(time.time() - start_time, 4)
        row_count = len(df)

        # ===============================
        # Step 5: Explain SQL
        # ===============================

        explanation = explain_sql(sql)

        return QueryResponse(
            sql=sql,
            result=df.to_dict(orient="records"),
            explanation=explanation,
            clarification=None,
            error=None,
            execution_time=execution_time,
            row_count=row_count
        )

    except Exception as e:
        logger.exception(f"[{request_id}] Error occurred")
        return QueryResponse(error=str(e))


# ===============================
# KPI DASHBOARD ENDPOINT
# ===============================

@router.get("/kpis")
def get_kpis():
    try:
        total_orders = executor.execute(
            "SELECT COUNT(*) AS total_orders FROM orders"
        )["total_orders"].iloc[0]

        total_customers = executor.execute(
            "SELECT COUNT(*) AS total_customers FROM customers"
        )["total_customers"].iloc[0]

        total_products = executor.execute(
            "SELECT COUNT(*) AS total_products FROM products"
        )["total_products"].iloc[0]

        total_payments = executor.execute(
            "SELECT COUNT(*) AS total_payments FROM payments"
        )["total_payments"].iloc[0]

        total_revenue = executor.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total_revenue
            FROM payments
            WHERE status = 'Completed'
            """
        )["total_revenue"].iloc[0]

        return {
            "total_orders": int(total_orders),
            "total_customers": int(total_customers),
            "total_products": int(total_products),
            "total_payments": int(total_payments),
            "total_revenue": float(total_revenue)
        }

    except Exception as e:
        logger.exception("Failed to load KPIs")
        return {"error": str(e)}
