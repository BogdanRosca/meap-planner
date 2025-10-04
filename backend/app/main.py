from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, recipes
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(title="Meal Planner API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Meal Planner API", "version": "1.0.0"}

# Include routers
app.include_router(health.router)
app.include_router(recipes.router)
