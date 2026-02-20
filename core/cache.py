import time

# Cache storage
_cache_store = {}

# 5 minute TTL
CACHE_TTL = 300  # seconds


def get_cached_response(question: str):
    key = question.strip().lower()

    if key in _cache_store:
        cached_data = _cache_store[key]

        # Check expiration
        if time.time() - cached_data["timestamp"] < CACHE_TTL:
            return cached_data["response"]

        # Expired → delete
        del _cache_store[key]

    return None


def set_cached_response(question: str, response: dict):
    key = question.strip().lower()

    _cache_store[key] = {
        "response": response,
        "timestamp": time.time()
    }
