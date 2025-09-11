"""
Database client for the Meal Planner application.
Handles all database connections and operations.
"""
import psycopg2
from typing import Optional, List, Dict, Any


class DatabaseClient:
    """Client for database operations"""
    
    def __init__(self, host: str = "localhost", port: str = "5432", 
                 database: str = "mealplanner", user: str = "bogdan.rosca", 
                 password: str = ""):
        """Initialize database client with connection parameters"""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self._connection = None
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def is_connected(self) -> bool:
        """Check if database connection is active"""
        if not self._connection:
            return False
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            return False
    
    def get_all_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes from the database"""
        if not self.is_connected():
            raise Exception("Not connected to database")
        
        cursor = self._connection.cursor()
        cursor.execute("""
            SELECT id, name, category, ingredients, instructions, prep_time, portions
            FROM recipes
            ORDER BY id
        """)
        
        recipes = []
        for row in cursor.fetchall():
            recipe = {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'ingredients': row[3],
                'instructions': row[4],
                'prep_time': row[5],
                'portions': row[6]
            }
            recipes.append(recipe)
        
        cursor.close()
        return recipes
