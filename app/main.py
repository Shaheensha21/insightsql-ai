from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import router
from app.logger import setup_logger

# Initialize logger
setup_logger()

app = FastAPI(title="InsightSQL AI")

# CORS (optional but safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}