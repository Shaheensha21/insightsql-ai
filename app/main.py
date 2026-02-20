from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.logger import setup_logger
from core.middleware import logging_middleware
from core.rate_limiter import rate_limit_middleware
from app.routes import router
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

# 🔹 Setup logging system
setup_logger()

# 🔹 Create FastAPI app
app = FastAPI(
    title="AI Text-to-SQL API",
    version="1.0.0"
)

# 🔹 Register middleware (ORDER MATTERS)
app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)

# 🔹 Include API routes
app.include_router(router)

# 🔹 Setup templates folder
templates = Jinja2Templates(directory="app/templates")


# 🔹 Home Page (Business UI)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🔹 Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
