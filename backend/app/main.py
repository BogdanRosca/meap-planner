from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, recipes

# Create FastAPI app instance
app = FastAPI(title="Meal Planner API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(recipes.router)
