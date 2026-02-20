import pandas as pd
from sqlalchemy import text
from core.db_connection import get_engine


class SQLExecutor:

    def __init__(self):
        self.engine = get_engine()

    def execute(self, query: str):
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
