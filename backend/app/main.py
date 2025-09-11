from fastapi import FastAPI

# Create FastAPI app instance
app = FastAPI(title="Meal Planner API", version="1.0.0")

@app.get("/health")
def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy", "message": "Meal Planner API is running !"}
