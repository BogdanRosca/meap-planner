"""
Unit tests for API endpoints using mocks
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app


# Create a test client
client = TestClient(app)


class TestGetAllRecipesEndpoint:
    """Test the GET /recipes endpoint"""
    
    @patch('app.main.DatabaseClient')
    def test_get_all_recipes_success(self, mock_db_client_class):
        """Test successful retrieval of all recipes"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_all_recipes.return_value = [
            {
                'id': 1,
                'name': 'Test Recipe',
                'category': 'dinner',
                'main_ingredients': [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}],
                'common_ingredients': ['salt', 'pepper'],
                'instructions': 'Cook it',
                'prep_time': 30,
                'portions': 4
            }
        ]
        
        # Make request
        response = client.get("/recipes")
        
        # Assertions
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == "success"
        assert json_response["count"] == 1
        assert len(json_response["recipes"]) == 1
        assert json_response["recipes"][0]["name"] == "Test Recipe"
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.get_all_recipes.assert_called_once()
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_get_all_recipes_connection_failure(self, mock_db_client_class):
        """Test handling of database connection failure"""
        # Setup mock to simulate connection failure
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = False
        
        # Make request
        response = client.get("/recipes")
        
        # Assertions - the HTTPException is raised directly, not caught by general exception handler
        assert response.status_code == 500
        json_response = response.json()
        assert "Failed to connect to database" in json_response["detail"]
        
        # Verify disconnect is still called
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_get_all_recipes_database_error(self, mock_db_client_class):
        """Test handling of database errors during recipe retrieval"""
        # Setup mock to simulate database error
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_all_recipes.side_effect = Exception("Database error")
        
        # Make request
        response = client.get("/recipes")
        
        # Assertions
        assert response.status_code == 500
        json_response = response.json()
        assert "Error retrieving recipes" in json_response["detail"]
        assert "Database error" in json_response["detail"]
        
        # Verify disconnect is still called
        mock_db_client.disconnect.assert_called_once()


class TestCreateRecipeEndpoint:
    """Test the POST /recipes endpoint"""
    
    @patch('app.main.DatabaseClient')
    def test_create_recipe_success(self, mock_db_client_class):
        """Test successful recipe creation"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.add_recipe.return_value = {
            'id': 123,
            'name': 'New Recipe',
            'category': 'lunch',
            'main_ingredients': [{'quantity': 200, 'unit': 'g', 'name': 'rice'}],
            'common_ingredients': ['salt'],
            'instructions': 'Cook rice',
            'prep_time': 20,
            'portions': 2
        }
        
        # Prepare request data
        recipe_data = {
            "name": "New Recipe",
            "category": "lunch",
            "main_ingredients": [
                {"quantity": 200, "unit": "g", "name": "rice"}
            ],
            "common_ingredients": ["salt"],
            "instructions": "Cook rice",
            "prep_time": 20,
            "portions": 2
        }
        
        # Make request
        response = client.post("/recipes", json=recipe_data)
        
        # Assertions
        assert response.status_code == 201
        json_response = response.json()
        assert json_response["status"] == "success"
        assert json_response["message"] == "Recipe created successfully"
        assert json_response["recipe_id"] == 123
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.add_recipe.assert_called_once()
        mock_db_client.disconnect.assert_called_once()
        
        # Verify the arguments passed to add_recipe
        call_args = mock_db_client.add_recipe.call_args
        assert call_args[1]['name'] == 'New Recipe'
        assert call_args[1]['category'] == 'lunch'
        assert call_args[1]['main_ingredients'] == [{'quantity': 200.0, 'unit': 'g', 'name': 'rice'}]
    
    @patch('app.main.DatabaseClient')
    def test_create_recipe_connection_failure(self, mock_db_client_class):
        """Test handling of database connection failure during recipe creation"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = False
        
        # Prepare request data
        recipe_data = {
            "name": "New Recipe",
            "category": "lunch",
            "main_ingredients": [{"quantity": 200, "unit": "g", "name": "rice"}],
            "common_ingredients": ["salt"],
            "instructions": "Cook rice",
            "prep_time": 20,
            "portions": 2
        }
        
        # Make request
        response = client.post("/recipes", json=recipe_data)
        
        # Assertions - the HTTPException is raised directly, not caught by general exception handler
        assert response.status_code == 500
        json_response = response.json()
        assert "Failed to connect to database" in json_response["detail"]
    
    def test_create_recipe_invalid_data(self):
        """Test validation of invalid recipe data"""
        # Invalid data - missing required fields
        invalid_recipe_data = {
            "name": "Incomplete Recipe",
            # missing category, main_ingredients, etc.
        }
        
        # Make request
        response = client.post("/recipes", json=invalid_recipe_data)
        
        # Should return validation error
        assert response.status_code == 422  # Unprocessable Entity
        json_response = response.json()
        assert "detail" in json_response
    
    def test_create_recipe_invalid_ingredient(self):
        """Test validation of invalid ingredient data"""
        # Invalid ingredient data
        invalid_recipe_data = {
            "name": "Recipe with Invalid Ingredient",
            "category": "dinner",
            "main_ingredients": [
                {"quantity": "not-a-number", "unit": "g", "name": "pasta"}  # invalid quantity
            ],
            "common_ingredients": ["salt"],
            "instructions": "Cook it",
            "prep_time": 30,
            "portions": 4
        }
        
        # Make request
        response = client.post("/recipes", json=invalid_recipe_data)
        
        # Should return validation error
        assert response.status_code == 422
        json_response = response.json()
        assert "detail" in json_response