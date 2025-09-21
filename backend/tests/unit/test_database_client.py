"""
Unit tests for DatabaseClient methods using mocks
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import psycopg2
from app.database_client import DatabaseClient


class TestDatabaseClientConnection:
    """Test DatabaseClient connection methods"""
    
    @patch('app.database_client.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        """Test successful database connection"""
        # Setup mock
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        # Create client and connect
        client = DatabaseClient()
        result = client.connect()
        
        # Assertions
        assert result is True
        assert client._connection == mock_connection
        mock_connect.assert_called_once()
    
    @patch('app.database_client.psycopg2.connect')
    def test_connect_failure(self, mock_connect):
        """Test database connection failure"""
        # Setup mock to raise exception
        mock_connect.side_effect = psycopg2.Error("Connection failed")
        
        # Create client and attempt connection
        client = DatabaseClient()
        result = client.connect()
        
        # Assertions
        assert result is False
        assert client._connection is None
    
    def test_disconnect(self):
        """Test database disconnection"""
        # Setup client with mock connection
        client = DatabaseClient()
        mock_connection = Mock()
        client._connection = mock_connection
        
        # Disconnect
        client.disconnect()
        
        # Assertions
        mock_connection.close.assert_called_once()
        assert client._connection is None
    
    def test_disconnect_no_connection(self):
        """Test disconnection when no connection exists"""
        client = DatabaseClient()
        client._connection = None
        
        # Should not raise an error
        client.disconnect()
        assert client._connection is None
    
    def test_is_connected_true(self):
        """Test is_connected when connection is active"""
        client = DatabaseClient()
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        client._connection = mock_connection
        
        result = client.is_connected()
        
        assert result is True
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT 1")
        mock_cursor.close.assert_called_once()
    
    def test_is_connected_false_no_connection(self):
        """Test is_connected when no connection exists"""
        client = DatabaseClient()
        client._connection = None
        
        result = client.is_connected()
        
        assert result is False
    
    @patch('app.database_client.psycopg2.Error', psycopg2.Error)
    def test_is_connected_false_error(self):
        """Test is_connected when connection has error"""
        client = DatabaseClient()
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = psycopg2.Error("Connection lost")
        mock_connection.cursor.return_value = mock_cursor
        client._connection = mock_connection
        
        result = client.is_connected()
        
        assert result is False


class TestDatabaseClientGetAllRecipes:
    """Test DatabaseClient get_all_recipes method"""
    
    def test_get_all_recipes_success(self):
        """Test successful retrieval of all recipes"""
        # Setup client with mock connection
        client = DatabaseClient()
        mock_connection = Mock()
        mock_cursor = Mock()
        
        # Mock database response
        mock_cursor.fetchall.return_value = [
            (1, 'Test Recipe', 'dinner', 
             [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}],
             ['salt', 'pepper'], 
             'Cook it', 30, 4)
        ]
        
        mock_connection.cursor.return_value = mock_cursor
        client._connection = mock_connection
        
        # Mock is_connected to return True
        with patch.object(client, 'is_connected', return_value=True):
            recipes = client.get_all_recipes()
        
        # Assertions
        assert len(recipes) == 1
        recipe = recipes[0]
        assert recipe['id'] == 1
        assert recipe['name'] == 'Test Recipe'
        assert recipe['category'] == 'dinner'
        assert recipe['main_ingredients'] == [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}]
        assert recipe['common_ingredients'] == ['salt', 'pepper']
        assert recipe['instructions'] == 'Cook it'
        assert recipe['prep_time'] == 30
        assert recipe['portions'] == 4
        
        # Verify SQL query
        mock_cursor.execute.assert_called_once()
        sql_call = mock_cursor.execute.call_args[0][0]
        assert "SELECT id, name, category, main_ingredients, common_ingredients, instructions, prep_time, portions" in sql_call
        assert "FROM recipes" in sql_call
        
        mock_cursor.close.assert_called_once()
    
    def test_get_all_recipes_not_connected(self):
        """Test get_all_recipes when not connected to database"""
        client = DatabaseClient()
        client._connection = None
        
        # Mock is_connected to return False
        with patch.object(client, 'is_connected', return_value=False):
            with pytest.raises(Exception) as exc_info:
                client.get_all_recipes()
        
        assert "Not connected to database" in str(exc_info.value)


class TestDatabaseClientAddRecipe:
    """Test DatabaseClient add_recipe method"""
    
    def test_add_recipe_success(self):
        """Test successful recipe addition"""
        # Setup client with mock connection
        client = DatabaseClient()
        mock_connection = Mock()
        mock_cursor = Mock()
        
        # Mock database response for RETURNING clause
        mock_cursor.fetchone.return_value = (
            123, 'New Recipe', 'lunch',
            [{'quantity': 200, 'unit': 'g', 'name': 'rice'}],
            ['salt'], 
            'Cook rice', 20, 2
        )
        
        mock_connection.cursor.return_value = mock_cursor
        client._connection = mock_connection
        
        # Test data
        main_ingredients = [{'quantity': 200, 'unit': 'g', 'name': 'rice'}]
        common_ingredients = ['salt']
        
        # Mock is_connected to return True
        with patch.object(client, 'is_connected', return_value=True):
            result = client.add_recipe(
                name='New Recipe',
                category='lunch',
                main_ingredients=main_ingredients,
                common_ingredients=common_ingredients,
                instructions='Cook rice',
                prep_time=20,
                portions=2
            )
        
        # Assertions
        assert result['id'] == 123
        assert result['name'] == 'New Recipe'
        assert result['category'] == 'lunch'
        assert result['main_ingredients'] == main_ingredients
        assert result['common_ingredients'] == common_ingredients
        
        # Verify SQL execution
        mock_cursor.execute.assert_called_once()
        sql_call = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO recipes" in sql_call
        assert "RETURNING" in sql_call
        
        # Verify parameters were passed correctly
        params = mock_cursor.execute.call_args[0][1]
        assert params[0] == 'New Recipe'  # name
        assert params[1] == 'lunch'       # category
        # params[2] should be JSON string of main_ingredients
        assert 'rice' in params[2]  # JSON contains rice
        assert params[3] == common_ingredients  # common_ingredients
        
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_add_recipe_not_connected(self):
        """Test add_recipe when not connected to database"""
        client = DatabaseClient()
        client._connection = None
        
        # Mock is_connected to return False
        with patch.object(client, 'is_connected', return_value=False):
            with pytest.raises(Exception) as exc_info:
                client.add_recipe(
                    name='Test',
                    category='lunch',
                    main_ingredients=[],
                    common_ingredients=[],
                    instructions='Test',
                    prep_time=10,
                    portions=1
                )
        
        assert "Not connected to database" in str(exc_info.value)


class TestDatabaseClientInitialization:
    """Test DatabaseClient initialization"""
    
    @patch.dict('os.environ', {
        'DB_HOST': 'test_host',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_pass'
    })
    def test_init_with_env_variables(self):
        """Test initialization with environment variables"""
        client = DatabaseClient()
        
        assert client.host == 'test_host'
        assert client.port == '5432'
        assert client.database == 'test_db'
        assert client.user == 'test_user'
        assert client.password == 'test_pass'
        assert client._connection is None
    
    def test_init_with_parameters(self):
        """Test initialization with explicit parameters"""
        client = DatabaseClient(
            host='param_host',
            port='1234',
            database='param_db',
            user='param_user',
            password='param_pass'
        )
        
        assert client.host == 'param_host'
        assert client.port == '1234'
        assert client.database == 'param_db'
        assert client.user == 'param_user'
        assert client.password == 'param_pass'