"""
Integration tests for update recipe functionality
"""
import pytest
from app.database_client import DatabaseClient


class TestUpdateRecipeIntegration:
    """Test the update_recipe functionality with real database operations"""
    
    def test_update_recipe_name_and_prep_time(self, db_client):
        """Test updating recipe name and prep time"""
        # Connect to database
        db_client.connect()
        
        # First, add a recipe to update
        original_recipe = db_client.add_recipe(
            name="Original Recipe",
            category="dinner",
            main_ingredients=[{"quantity": 250, "unit": "g", "name": "pasta"}],
            common_ingredients=["salt", "pepper"],
            instructions="Cook the pasta",
            prep_time=20,
            portions=4
        )
        
        recipe_id = original_recipe['id']
        
        # Update the recipe
        updates = {
            'name': 'Updated Recipe Name',
            'prep_time': 30
        }
        
        updated_recipe = db_client.update_recipe(recipe_id, updates)
        
        # Assertions
        assert updated_recipe is not None
        assert updated_recipe['id'] == recipe_id
        assert updated_recipe['name'] == 'Updated Recipe Name'
        assert updated_recipe['prep_time'] == 30
        # Other fields should remain unchanged
        assert updated_recipe['category'] == 'dinner'
        assert updated_recipe['instructions'] == 'Cook the pasta'
        assert updated_recipe['portions'] == 4
        
        # Verify the update persisted by retrieving the recipe again
        retrieved_recipe = db_client.get_recipe_by_id(recipe_id)
        assert retrieved_recipe['name'] == 'Updated Recipe Name'
        assert retrieved_recipe['prep_time'] == 30
    
    def test_update_recipe_ingredients(self, db_client):
        """Test updating recipe ingredients"""
        # Connect to database
        db_client.connect()
        
        # Add a recipe to update
        original_recipe = db_client.add_recipe(
            name="Test Recipe",
            category="lunch",
            main_ingredients=[{"quantity": 250, "unit": "g", "name": "pasta"}],
            common_ingredients=["salt", "pepper"],
            instructions="Cook it",
            prep_time=15,
            portions=2
        )
        
        recipe_id = original_recipe['id']
        
        # Update ingredients
        updates = {
            'main_ingredients': [
                {"quantity": 200, "unit": "g", "name": "rice"},
                {"quantity": 100, "unit": "g", "name": "chicken"}
            ],
            'common_ingredients': ["garlic", "onion", "ginger"]
        }
        
        updated_recipe = db_client.update_recipe(recipe_id, updates)
        
        # Assertions
        assert updated_recipe is not None
        assert len(updated_recipe['main_ingredients']) == 2
        assert updated_recipe['main_ingredients'][0]['name'] == 'rice'
        assert updated_recipe['main_ingredients'][1]['name'] == 'chicken'
        assert updated_recipe['common_ingredients'] == ["garlic", "onion", "ginger"]
        
        # Other fields should remain unchanged
        assert updated_recipe['name'] == 'Test Recipe'
        assert updated_recipe['category'] == 'lunch'
        assert updated_recipe['prep_time'] == 15
    
    def test_update_recipe_all_fields(self, db_client):
        """Test updating all recipe fields"""
        # Connect to database
        db_client.connect()
        
        # Add a recipe to update
        original_recipe = db_client.add_recipe(
            name="Original Recipe",
            category="breakfast",
            main_ingredients=[{"quantity": 100, "unit": "g", "name": "oats"}],
            common_ingredients=["milk"],
            instructions="Mix and serve",
            prep_time=5,
            portions=1
        )
        
        recipe_id = original_recipe['id']
        
        # Update all fields
        updates = {
            'name': 'Completely New Recipe',
            'category': 'dinner',
            'main_ingredients': [
                {"quantity": 300, "unit": "g", "name": "beef"},
                {"quantity": 200, "unit": "g", "name": "potatoes"}
            ],
            'common_ingredients': ["salt", "pepper", "herbs"],
            'instructions': 'Season beef, roast with potatoes',
            'prep_time': 60,
            'portions': 4
        }
        
        updated_recipe = db_client.update_recipe(recipe_id, updates)
        
        # Assertions - all fields should be updated
        assert updated_recipe is not None
        assert updated_recipe['id'] == recipe_id
        assert updated_recipe['name'] == 'Completely New Recipe'
        assert updated_recipe['category'] == 'dinner'
        assert len(updated_recipe['main_ingredients']) == 2
        assert updated_recipe['main_ingredients'][0]['name'] == 'beef'
        assert updated_recipe['main_ingredients'][1]['name'] == 'potatoes'
        assert updated_recipe['common_ingredients'] == ["salt", "pepper", "herbs"]
        assert updated_recipe['instructions'] == 'Season beef, roast with potatoes'
        assert updated_recipe['prep_time'] == 60
        assert updated_recipe['portions'] == 4
    
    def test_update_nonexistent_recipe(self, db_client):
        """Test updating a recipe that doesn't exist"""
        # Connect to database
        db_client.connect()
        
        # Try to update a recipe that doesn't exist
        updates = {'name': 'This should fail'}
        result = db_client.update_recipe(99999, updates)
        
        # Should return None
        assert result is None
    
    def test_update_recipe_empty_updates(self, db_client):
        """Test updating with no valid fields"""
        # Connect to database
        db_client.connect()
        
        # Add a recipe
        original_recipe = db_client.add_recipe(
            name="Test Recipe",
            category="dinner",
            main_ingredients=[{"quantity": 250, "unit": "g", "name": "pasta"}],
            common_ingredients=["salt"],
            instructions="Cook it",
            prep_time=20,
            portions=2
        )
        
        recipe_id = original_recipe['id']
        
        # Try to update with invalid fields
        updates = {'invalid_field': 'value', 'another_invalid': 123}
        result = db_client.update_recipe(recipe_id, updates)
        
        # Should return None since no valid fields to update
        assert result is None
        
        # Original recipe should remain unchanged
        unchanged_recipe = db_client.get_recipe_by_id(recipe_id)
        assert unchanged_recipe['name'] == 'Test Recipe'
        assert unchanged_recipe['prep_time'] == 20
    
    def test_update_recipe_partial_ingredients(self, db_client):
        """Test updating only main_ingredients while keeping common_ingredients"""
        # Connect to database
        db_client.connect()
        
        # Add a recipe
        original_recipe = db_client.add_recipe(
            name="Test Recipe",
            category="dinner",
            main_ingredients=[{"quantity": 250, "unit": "g", "name": "pasta"}],
            common_ingredients=["salt", "pepper"],
            instructions="Cook it",
            prep_time=20,
            portions=2
        )
        
        recipe_id = original_recipe['id']
        
        # Update only main_ingredients
        updates = {
            'main_ingredients': [
                {"quantity": 300, "unit": "g", "name": "rice"}
            ]
        }
        
        updated_recipe = db_client.update_recipe(recipe_id, updates)
        
        # Assertions
        assert updated_recipe is not None
        assert len(updated_recipe['main_ingredients']) == 1
        assert updated_recipe['main_ingredients'][0]['name'] == 'rice'
        assert updated_recipe['main_ingredients'][0]['quantity'] == 300
        
        # common_ingredients should remain unchanged
        assert updated_recipe['common_ingredients'] == ["salt", "pepper"]
        
        # Other fields should remain unchanged
        assert updated_recipe['name'] == 'Test Recipe'
        assert updated_recipe['prep_time'] == 20