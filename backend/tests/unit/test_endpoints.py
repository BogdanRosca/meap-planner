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


class TestDeleteRecipeEndpoint:
    """Test the DELETE /recipes/{recipe_id} endpoint"""
    
    @patch('app.main.DatabaseClient')
    def test_delete_recipe_success(self, mock_db_client_class):
        """Test successful recipe deletion"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.delete_recipe.return_value = True
        
        # Make request
        response = client.delete("/recipes/123")
        
        # Assertions
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == "success"
        assert "deleted successfully" in json_response["message"]
        assert "123" in json_response["message"]
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.delete_recipe.assert_called_once_with(123)
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_delete_recipe_not_found(self, mock_db_client_class):
        """Test deletion of non-existent recipe"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.delete_recipe.return_value = False  # Recipe not found
        
        # Make request
        response = client.delete("/recipes/999")
        
        # Assertions
        assert response.status_code == 404
        json_response = response.json()
        assert "Recipe with ID 999 not found" in json_response["detail"]
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.delete_recipe.assert_called_once_with(999)
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_delete_recipe_connection_failure(self, mock_db_client_class):
        """Test handling of database connection failure during recipe deletion"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = False
        
        # Make request
        response = client.delete("/recipes/123")
        
        # Assertions
        assert response.status_code == 500
        json_response = response.json()
        assert "Failed to connect to database" in json_response["detail"]
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.delete_recipe.assert_not_called()  # Should not be called if connection fails
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_delete_recipe_database_error(self, mock_db_client_class):
        """Test handling of database error during recipe deletion"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.delete_recipe.side_effect = Exception("Database error")
        
        # Make request
        response = client.delete("/recipes/123")
        
        # Assertions
        assert response.status_code == 500
        json_response = response.json()
        assert "Error deleting recipe" in json_response["detail"]
        assert "Database error" in json_response["detail"]
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.delete_recipe.assert_called_once_with(123)
        mock_db_client.disconnect.assert_called_once()
    
    def test_delete_recipe_invalid_id(self):
        """Test deletion with invalid recipe ID"""
        # Make request with invalid ID (non-integer)
        response = client.delete("/recipes/not-a-number")
        
        # Should return validation error
        assert response.status_code == 422  # Unprocessable Entity
        json_response = response.json()
        assert "detail" in json_response


class TestGetRecipeByIdEndpoint:
    """Test the GET /recipes/{recipe_id} endpoint"""
    
    @patch('app.main.DatabaseClient')
    def test_get_recipe_by_id_success(self, mock_db_client_class):
        """Test successful retrieval of a recipe by ID"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_recipe_by_id.return_value = {
            'id': 1,
            'name': 'Test Recipe',
            'category': 'dinner',
            'main_ingredients': [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}],
            'common_ingredients': ['salt', 'pepper'],
            'instructions': 'Cook it',
            'prep_time': 30,
            'portions': 4
        }
        
        # Make request
        response = client.get("/recipes/1")
        
        # Assertions
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["id"] == 1
        assert json_response["name"] == "Test Recipe"
        assert json_response["category"] == "dinner"
        assert json_response["main_ingredients"] == [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}]
        assert json_response["common_ingredients"] == ['salt', 'pepper']
        assert json_response["instructions"] == "Cook it"
        assert json_response["prep_time"] == 30
        assert json_response["portions"] == 4
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.get_recipe_by_id.assert_called_once_with(1)
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_get_recipe_by_id_not_found(self, mock_db_client_class):
        """Test retrieval of non-existent recipe"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_recipe_by_id.return_value = None
        
        # Make request
        response = client.get("/recipes/999")
        
        # Assertions
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["detail"] == "Recipe with ID 999 not found"
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.get_recipe_by_id.assert_called_once_with(999)
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_get_recipe_by_id_database_connection_error(self, mock_db_client_class):
        """Test recipe retrieval when database connection fails"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = False
        
        # Make request
        response = client.get("/recipes/1")
        
        # Assertions
        assert response.status_code == 500
        json_response = response.json()
        assert json_response["detail"] == "Failed to connect to database"
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.get_recipe_by_id.assert_not_called()
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_get_recipe_by_id_database_error(self, mock_db_client_class):
        """Test recipe retrieval when database operation fails"""
        # Setup mock
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_recipe_by_id.side_effect = Exception("Database error")
        
        # Make request
        response = client.get("/recipes/1")
        
        # Assertions
        assert response.status_code == 500
        json_response = response.json()
        assert "Error retrieving recipe" in json_response["detail"]
        assert "Database error" in json_response["detail"]
        
        # Verify mock calls
        mock_db_client.connect.assert_called_once()
        mock_db_client.get_recipe_by_id.assert_called_once_with(1)
        mock_db_client.disconnect.assert_called_once()
    
    def test_get_recipe_by_id_invalid_id(self):
        """Test retrieval with invalid recipe ID"""
        # Make request with invalid ID (non-integer)
        response = client.get("/recipes/not-a-number")
        
        # Should return validation error
        assert response.status_code == 422  # Unprocessable Entity
        json_response = response.json()
        assert "detail" in json_response