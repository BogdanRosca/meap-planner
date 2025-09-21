"""
Unit tests for error handling and edge cases
"""
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.database_client import DatabaseClient


# Create a test client
client = TestClient(app)


class TestErrorHandling:
    """Test error handling across the application"""
    
    @patch('app.main.DatabaseClient')
    def test_get_recipes_unexpected_exception(self, mock_db_client_class):
        """Test handling of unexpected exceptions in get_all_recipes"""
        # Setup mock to raise unexpected exception
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_all_recipes.side_effect = RuntimeError("Unexpected error")
        
        # Make request
        response = client.get("/recipes")
        
        # Should handle gracefully
        assert response.status_code == 500
        json_response = response.json()
        assert "Error retrieving recipes" in json_response["detail"]
        assert "Unexpected error" in json_response["detail"]
        
        # Ensure cleanup happens
        mock_db_client.disconnect.assert_called_once()
    
    @patch('app.main.DatabaseClient')
    def test_create_recipe_unexpected_exception(self, mock_db_client_class):
        """Test handling of unexpected exceptions in create_recipe"""
        # Setup mock to raise unexpected exception
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.add_recipe.side_effect = RuntimeError("Database exploded")
        
        # Prepare valid request data
        recipe_data = {
            "name": "Test Recipe",
            "category": "dinner",
            "main_ingredients": [{"quantity": 250, "unit": "g", "name": "pasta"}],
            "common_ingredients": ["salt"],
            "instructions": "Cook it",
            "prep_time": 30,
            "portions": 4
        }
        
        # Make request
        response = client.post("/recipes", json=recipe_data)
        
        # Should handle gracefully
        assert response.status_code == 500
        json_response = response.json()
        assert "Error creating recipe" in json_response["detail"]
        assert "Database exploded" in json_response["detail"]
        
        # Ensure cleanup happens
        mock_db_client.disconnect.assert_called_once()


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    @patch('app.main.DatabaseClient')
    def test_get_recipes_empty_result(self, mock_db_client_class):
        """Test handling when database returns empty recipe list"""
        # Setup mock to return empty list
        mock_db_client = Mock()
        mock_db_client_class.return_value = mock_db_client
        mock_db_client.connect.return_value = True
        mock_db_client.get_all_recipes.return_value = []
        
        # Make request
        response = client.get("/recipes")
        
        # Should handle gracefully
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == "success"
        assert json_response["count"] == 0
        assert json_response["recipes"] == []
    
    def test_create_recipe_with_edge_case_values(self):
        """Test recipe creation with edge case values"""
        # Test with extreme but valid values
        recipe_data = {
            "name": "A" * 255,  # Very long name
            "category": "breakfast",
            "main_ingredients": [
                {"quantity": 0.001, "unit": "mg", "name": "x"},  # Very small quantity
                {"quantity": 9999.999, "unit": "kg", "name": "y"}  # Very large quantity
            ],
            "common_ingredients": [],  # Empty list
            "instructions": "X",  # Minimal instructions
            "prep_time": 0,  # Zero prep time
            "portions": 1  # Minimum portions
        }
        
        with patch('app.main.DatabaseClient') as mock_db_client_class:
            mock_db_client = Mock()
            mock_db_client_class.return_value = mock_db_client
            mock_db_client.connect.return_value = True
            mock_db_client.add_recipe.return_value = {"id": 1, **recipe_data}
            
            response = client.post("/recipes", json=recipe_data)
            
            # Should handle edge cases successfully
            assert response.status_code == 201
    
    def test_create_recipe_with_unicode_characters(self):
        """Test recipe creation with unicode characters"""
        recipe_data = {
            "name": "Crème Brûlée with émmental 🧀",
            "category": "dinner",
            "main_ingredients": [
                {"quantity": 250, "unit": "g", "name": "émmental cheese"},
                {"quantity": 2, "unit": "cups", "name": "crème fraîche"}
            ],
            "common_ingredients": ["salt", "poivre noir", "herbes de Provence"],
            "instructions": "Mélanger délicatement les ingrédients...",
            "prep_time": 45,
            "portions": 6
        }
        
        with patch('app.main.DatabaseClient') as mock_db_client_class:
            mock_db_client = Mock()
            mock_db_client_class.return_value = mock_db_client
            mock_db_client.connect.return_value = True
            mock_db_client.add_recipe.return_value = {"id": 1, **recipe_data}
            
            response = client.post("/recipes", json=recipe_data)
            
            # Should handle unicode successfully
            assert response.status_code == 201
    
    def test_create_recipe_with_many_ingredients(self):
        """Test recipe creation with many ingredients"""
        # Create a recipe with many ingredients
        main_ingredients = [
            {"quantity": i, "unit": "g", "name": f"ingredient_{i}"}
            for i in range(1, 21)  # 20 ingredients
        ]
        
        common_ingredients = [f"common_{i}" for i in range(1, 11)]  # 10 common ingredients
        
        recipe_data = {
            "name": "Complex Recipe",
            "category": "dinner",
            "main_ingredients": main_ingredients,
            "common_ingredients": common_ingredients,
            "instructions": "Mix everything together",
            "prep_time": 120,
            "portions": 8
        }
        
        with patch('app.main.DatabaseClient') as mock_db_client_class:
            mock_db_client = Mock()
            mock_db_client_class.return_value = mock_db_client
            mock_db_client.connect.return_value = True
            mock_db_client.add_recipe.return_value = {"id": 1, **recipe_data}
            
            response = client.post("/recipes", json=recipe_data)
            
            # Should handle many ingredients successfully
            assert response.status_code == 201


class TestDatabaseClientEdgeCases:
    """Test DatabaseClient edge cases"""
    
    @patch.dict('os.environ', {}, clear=True)  # Clear all environment variables
    @patch('app.database_client.load_dotenv')  # Prevent loading .env file
    def test_database_client_with_none_values(self, mock_load_dotenv):
        """Test DatabaseClient initialization with None values"""
        # Test that None values are handled gracefully
        client = DatabaseClient(
            host=None,
            port=None,
            database=None,
            user=None,
            password=None
        )
        
        # Should get None values since no env vars are set and explicit params are None
        # Note: os.getenv returns None when env var doesn't exist
        assert client.host is None
        assert client.port is None
        assert client.database is None
        assert client.user is None
        assert client.password is None
    
    def test_add_recipe_with_empty_json(self):
        """Test add_recipe with empty main_ingredients"""
        client = DatabaseClient()
        mock_connection = Mock()
        mock_cursor = Mock()
        
        # Mock successful response
        mock_cursor.fetchone.return_value = (
            1, 'Empty Recipe', 'snack', [], [], 'No cooking', 0, 1
        )
        
        mock_connection.cursor.return_value = mock_cursor
        client._connection = mock_connection
        
        with patch.object(client, 'is_connected', return_value=True):
            result = client.add_recipe(
                name='Empty Recipe',
                category='snack',
                main_ingredients=[],  # Empty list
                common_ingredients=[],  # Empty list
                instructions='No cooking',
                prep_time=0,
                portions=1
            )
        
        # Should handle empty ingredients successfully
        assert result['name'] == 'Empty Recipe'
        assert result['main_ingredients'] == []
        assert result['common_ingredients'] == []