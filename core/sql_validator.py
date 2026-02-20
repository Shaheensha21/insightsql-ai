import re

class SQLValidator:

    def validate(self, query: str):
        """
        Returns:
            (True, None) if valid
            (False, error_message) if invalid
        """

        if not query:
            return False, "Empty SQL query"

        query = query.strip().lower()

        # Allow only SELECT queries
        if not query.startswith("select"):
            return False, "Only SELECT queries are allowed"

        # Block dangerous keywords
        forbidden = [
            "insert", "update", "delete",
            "drop", "alter", "truncate",
            "create", "grant", "revoke"
        ]

        for word in forbidden:
            if re.search(rf"\b{word}\b", query):
                return False, f"Forbidden keyword detected: {word}"

        return True, None
