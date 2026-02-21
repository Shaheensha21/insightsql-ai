from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.logger import setup_logger
from core.middleware import logging_middleware
from core.rate_limiter import rate_limit_middleware
from app.routes import router

# Setup logging
setup_logger()

app = FastAPI(title="AI Text-to-SQL API", version="1.0.0")

# Register middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)

# Include routes
app.include_router(router)

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    return {"status": "healthy"}