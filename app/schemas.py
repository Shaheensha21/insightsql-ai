from pydantic import BaseModel
from typing import Optional, List, Dict, Any


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
