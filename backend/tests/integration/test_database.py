"""
Integration tests for database connectivity
"""
import os
import pytest
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestDatabaseConnection:
    """Test database connection and basic operations"""
    
    @pytest.fixture
    def db_connection(self):
        """Create a database connection for testing"""
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        yield connection
        connection.close()
    
    def test_database_connection(self, db_connection):
        """Test that we can connect to the database"""
        assert db_connection is not None
        
        # Test that the connection is working
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        
        assert result[0] == 1
    
    def test_recipes_table_exists(self, db_connection):
        """Test that the recipes table exists"""
        cursor = db_connection.cursor()
        
        # Check if recipes table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'recipes'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        cursor.close()
        
        assert table_exists is True
