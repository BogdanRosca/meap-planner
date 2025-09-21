from fastapi import FastAPI
from .routes import health, recipes

# Create FastAPI app instance
app = FastAPI(title="Meal Planner API", version="1.0.0")

# Include routers
app.include_router(health.router)
app.include_router(recipes.router)
