"""
Tests for the database client
"""
import pytest
from app.database_client import DatabaseClient


class TestDatabaseClient:
    """Test the database client functionality"""
    
    @pytest.fixture
    def db_client(self):
        """Create a database client for testing"""
        client = DatabaseClient()
        yield client
        client.disconnect()
    
    def test_client_connection(self, db_client):
        """Test that the client can connect to the database"""
        # Test connection
        success = db_client.connect()
        assert success is True
        
        # Test is_connected method
        assert db_client.is_connected() is True
        
        # Test disconnection
        db_client.disconnect()
        assert db_client.is_connected() is False
    
    def test_get_all_recipes(self, db_client):
        """Test that we can retrieve all recipes"""
        # Connect to database
        db_client.connect()
        
        # Get all recipes
        recipes = db_client.get_all_recipes()
        
        # Should be a list
        assert isinstance(recipes, list)
        
        # Should have at least one recipe (the one we inserted)
        assert len(recipes) >= 1
        
        # Check the structure of the first recipe
        if len(recipes) > 0:
            recipe = recipes[0]
            required_fields = ['id', 'name', 'category', 'ingredients', 'instructions', 'prep_time', 'portions']
            for field in required_fields:
                assert field in recipe
