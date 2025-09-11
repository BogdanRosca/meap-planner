from fastapi import FastAPI, HTTPException
from .database_client import DatabaseClient

# Create FastAPI app instance
app = FastAPI(title="Meal Planner API", version="1.0.0")

@app.get("/health")
def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy", "message": "Meal Planner API is running !"}

@app.get("/recipes")
def get_all_recipes():
    """Get all recipes from the database"""
    # Create database client
    db_client = DatabaseClient()
    
    try:
        # Connect to database
        if not db_client.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Get all recipes
        recipes = db_client.get_all_recipes()
        
        return {
            "status": "success",
            "count": len(recipes),
            "recipes": recipes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recipes: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()
