"""
Shared test configuration and fixtures for unit tests
"""
import pytest
from unittest.mock import Mock


# Common test data for recipes
SAMPLE_RECIPE_1 = {
    'id': 1,
    'name': 'Test Recipe',
    'category': 'dinner',
    'main_ingredients': [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}],
    'common_ingredients': ['salt', 'pepper'],
    'instructions': 'Cook it',
    'prep_time': 30,
    'portions': 4
}

SAMPLE_RECIPE_2 = {
    'id': 123,
    'name': 'New Recipe',
    'category': 'lunch',
    'main_ingredients': [{'quantity': 200, 'unit': 'g', 'name': 'rice'}],
    'common_ingredients': ['salt'],
    'instructions': 'Cook rice',
    'prep_time': 20,
    'portions': 2
}

# Test data for creating recipes (without ID)
CREATE_RECIPE_DATA = {
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

# Test data for updating recipes
UPDATE_RECIPE_DATA = {
    'name': 'Updated Recipe Name',
    'prep_time': 35,
    'instructions': 'Updated instructions'
}

UPDATE_RECIPE_WITH_INGREDIENTS_DATA = {
    'main_ingredients': [
        {'quantity': 200, 'unit': 'g', 'name': 'rice'}
    ],
    'common_ingredients': ['garlic', 'onion']
}

# Updated recipe response after successful update
UPDATED_RECIPE_RESPONSE = {
    'id': 1,
    'name': 'Updated Recipe Name',
    'category': 'dinner',
    'main_ingredients': [{'quantity': 250, 'unit': 'g', 'name': 'pasta'}],
    'common_ingredients': ['salt', 'pepper'],
    'instructions': 'Updated instructions',
    'prep_time': 35,
    'portions': 4
}

# Updated recipe response after ingredient update
UPDATED_RECIPE_WITH_INGREDIENTS_RESPONSE = {
    'id': 1,
    'name': 'Test Recipe',
    'category': 'dinner',
    'main_ingredients': [{'quantity': 200, 'unit': 'g', 'name': 'rice'}],
    'common_ingredients': ['garlic', 'onion'],
    'instructions': 'Cook rice',
    'prep_time': 25,
    'portions': 2
}

# Invalid test data
INVALID_RECIPE_DATA_MISSING_FIELDS = {
    "name": "Incomplete Recipe",
    # missing category, main_ingredients, etc.
}

INVALID_RECIPE_DATA_INVALID_INGREDIENT = {
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

INVALID_UPDATE_DATA_TYPES = {
    'prep_time': 'not-a-number',  # Should be int
    'portions': 'also-not-a-number'  # Should be int
}


@pytest.fixture
def mock_db_client():
    """Create a mock database client for testing"""
    mock_client = Mock()
    mock_client.connect.return_value = True
    mock_client.disconnect.return_value = None
    return mock_client


@pytest.fixture
def mock_db_client_connection_failure():
    """Create a mock database client that fails to connect"""
    mock_client = Mock()
    mock_client.connect.return_value = False
    mock_client.disconnect.return_value = None
    return mock_client


@pytest.fixture
def mock_db_client_with_database_error():
    """Create a mock database client that raises database errors"""
    mock_client = Mock()
    mock_client.connect.return_value = True
    mock_client.disconnect.return_value = None
    return mock_client