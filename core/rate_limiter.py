import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse

# Store request timestamps per IP
request_logs = defaultdict(list)

# Configuration
MAX_REQUESTS = 5
WINDOW_SECONDS = 60


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    # Remove old requests outside time window
    request_logs[client_ip] = [
        timestamp
        for timestamp in request_logs[client_ip]
        if current_time - timestamp < WINDOW_SECONDS
    ]

    # Check limit
    if len(request_logs[client_ip]) >= MAX_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={"error": "Too many requests. Please try again later."}
        )

    # Log current request
    request_logs[client_ip].append(current_time)

    response = await call_next(request)
    return response
