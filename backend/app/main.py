from .database_client import DatabaseClient
from .models import Ingredient, RecipeCreate, RecipeUpdate, RecipeResponse, NewRecipeResponse
from fastapi import FastAPI, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse

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

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe_by_id(recipe_id: int):
    """Get a specific recipe by ID"""
    # Create database client
    db_client = DatabaseClient()
    
    try:
        # Connect to database
        if not db_client.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Get the recipe by ID
        recipe = db_client.get_recipe_by_id(recipe_id)
        
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
        
        return recipe
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recipe: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()

@app.post("/recipes", response_model=NewRecipeResponse)
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
        main_ingredients_dicts = [ingredient.model_dump() for ingredient in recipe.main_ingredients]
        
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
                "id": new_recipe["id"],
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

@app.patch("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(recipe_id: int, recipe_update: RecipeUpdate):
    """Update a recipe by ID with partial data"""
    # Create database client
    db_client = DatabaseClient()
    
    try:
        # Connect to database
        if not db_client.connect():
            raise HTTPException(status_code=500, detail="Failed to connect to database")
        
        # Convert update data to dict, excluding None values
        update_data = recipe_update.model_dump(exclude_unset=True)
        
        # If no fields to update, return error
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        # Convert Pydantic Ingredient objects to dictionaries if present
        # Note: model_dump() already converts nested Pydantic objects to dicts,
        # so main_ingredients is already a list of dicts at this point
        
        # Update the recipe
        updated_recipe = db_client.update_recipe(recipe_id, update_data)
        
        if not updated_recipe:
            raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
        
        return updated_recipe
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating recipe: {str(e)}")
    
    finally:
        # Always disconnect
        db_client.disconnect()
