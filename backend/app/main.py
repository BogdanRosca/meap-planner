from .database_client import DatabaseClient
from fastapi import FastAPI, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List


# Pydantic models for request/response validation
class Ingredient(BaseModel):
    quantity: float
    unit: str
    name: str

class RecipeCreate(BaseModel):
    name: str
    category: str
    main_ingredients: List[Ingredient]
    common_ingredients: List[str]
    instructions: str
    prep_time: int
    portions: int

class RecipeResponse(BaseModel):
    id: int
    name: str
    category: str
    main_ingredients: List[Ingredient]
    common_ingredients: List[str]
    instructions: str
    prep_time: int
    portions: int

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
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recipes: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()

@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe in the database"""
    # Create database client
    db_client = DatabaseClient()
    
    try:
        # Connect to database
        if not db_client.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Create the recipe
        # Convert Pydantic Ingredient objects to dictionaries
        main_ingredients_dicts = [ingredient.dict() for ingredient in recipe.main_ingredients]
        
        new_recipe = db_client.add_recipe(
            name=recipe.name,
            category=recipe.category,
            main_ingredients=main_ingredients_dicts,
            common_ingredients=recipe.common_ingredients,
            instructions=recipe.instructions,
            prep_time=recipe.prep_time,
            portions=recipe.portions
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "recipe_id": new_recipe["id"],
                "status": "success",
                "message": "Recipe created successfully"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating recipe: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    """Delete a recipe by ID"""
    # Create database client
    db_client = DatabaseClient()
    
    try:
        # Connect to database
        if not db_client.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Attempt to delete the recipe
        success = db_client.delete_recipe(recipe_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": f"Recipe with ID {recipe_id} deleted successfully"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting recipe: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()
