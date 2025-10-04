import React, { useState } from 'react';
import './App.css';

interface Recipe {
  id: number;
  name: string;
  category: string;
  main_ingredients: Array<{
    name: string;
    unit: string;
    quantity: number;
  }>;
  common_ingredients: string[];
  instructions: string;  
  prep_time: number;
  portions: number;
}

interface NewRecipe {
  name: string;
  category: string;
  main_ingredients: Array<{
    name: string;
    unit: string;
    quantity: number;
  }>;
  common_ingredients: string[];
  instructions: string;
  prep_time: number;
  portions: number;
}

function App() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [addingRecipe, setAddingRecipe] = useState(false);
  const [newRecipe, setNewRecipe] = useState<NewRecipe>({
    name: '',
    category: '',
    main_ingredients: [{ name: '', unit: '', quantity: 0 }],
    common_ingredients: [''],
    instructions: '',
    prep_time: 0,
    portions: 0
  });

  const fetchRecipes = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/recipes');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setRecipes(data.recipes || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching recipes:', err);
    } finally {
      setLoading(false);
    }
  };

  const addRecipe = async () => {
    setAddingRecipe(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRecipe),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setRecipes(prev => [...prev, data]);
      setNewRecipe({
        name: '',
        category: '',
        main_ingredients: [{ name: '', unit: '', quantity: 0 }],
        common_ingredients: [''],
        instructions: '',
        prep_time: 0,
        portions: 0
      });
      setShowAddForm(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error adding recipe:', err);
    } finally {
      setAddingRecipe(false);
    }
  };

  const addMainIngredient = () => {
    setNewRecipe(prev => ({
      ...prev,
      main_ingredients: [...prev.main_ingredients, { name: '', unit: '', quantity: 0 }]
    }));
  };

  const removeMainIngredient = (index: number) => {
    setNewRecipe(prev => ({
      ...prev,
      main_ingredients: prev.main_ingredients.filter((_, i) => i !== index)
    }));
  };

  const updateMainIngredient = (index: number, field: keyof typeof newRecipe.main_ingredients[0], value: string | number) => {
    setNewRecipe(prev => ({
      ...prev,
      main_ingredients: prev.main_ingredients.map((ingredient, i) => 
        i === index ? { ...ingredient, [field]: value } : ingredient
      )
    }));
  };

  const addCommonIngredient = () => {
    setNewRecipe(prev => ({
      ...prev,
      common_ingredients: [...prev.common_ingredients, '']
    }));
  };

  const removeCommonIngredient = (index: number) => {
    setNewRecipe(prev => ({
      ...prev,
      common_ingredients: prev.common_ingredients.filter((_, i) => i !== index)
    }));
  };

  const updateCommonIngredient = (index: number, value: string) => {
    setNewRecipe(prev => ({
      ...prev,
      common_ingredients: prev.common_ingredients.map((ingredient, i) => 
        i === index ? value : ingredient
      )
    }));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Meal Planner App</h1>
        <div className="button-group">
          <button 
            onClick={fetchRecipes}
            disabled={loading}
            className="fetch-button"
          >
            {loading ? 'Loading...' : 'Fetch Recipes'}
          </button>
          <button 
            onClick={() => setShowAddForm(!showAddForm)}
            className="add-button"
          >
            {showAddForm ? 'Cancel' : 'Add Recipe'}
          </button>
        </div>
        
        {error && (
          <div className="error">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {showAddForm && (
          <div className="add-recipe-form">
            <h2>Add New Recipe</h2>
            <form onSubmit={(e) => { e.preventDefault(); addRecipe(); }}>
              <div className="form-group">
                <label htmlFor="name">Recipe Name:</label>
                <input
                  type="text"
                  id="name"
                  value={newRecipe.name}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, name: e.target.value }))}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="category">Category:</label>
                <select
                  id="category"
                  value={newRecipe.category}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, category: e.target.value }))}
                  required
                >
                  <option value="">Select a category</option>
                  <option value="breakfast">Breakfast</option>
                  <option value="lunch">Lunch</option>
                  <option value="dinner">Dinner</option>
                  <option value="snack">Snack</option>
                  <option value="dessert">Dessert</option>
                </select>
              </div>

              <div className="form-group">
                <label>Main Ingredients:</label>
                {newRecipe.main_ingredients.map((ingredient, index) => (
                  <div key={index} className="ingredient-group">
                    <input
                      type="text"
                      placeholder="Ingredient name"
                      value={ingredient.name}
                      onChange={(e) => updateMainIngredient(index, 'name', e.target.value)}
                      required
                    />
                    <input
                      type="number"
                      placeholder="Quantity"
                      value={ingredient.quantity || ''}
                      onChange={(e) => updateMainIngredient(index, 'quantity', parseFloat(e.target.value) || 0)}
                      required
                    />
                    <input
                      type="text"
                      placeholder="Unit (g, pcs, ml, etc.)"
                      value={ingredient.unit}
                      onChange={(e) => updateMainIngredient(index, 'unit', e.target.value)}
                      required
                    />
                    {newRecipe.main_ingredients.length > 1 && (
                      <button type="button" onClick={() => removeMainIngredient(index)} className="remove-button">
                        Remove
                      </button>
                    )}
                  </div>
                ))}
                <button type="button" onClick={addMainIngredient} className="add-ingredient-button">
                  Add Main Ingredient
                </button>
              </div>

              <div className="form-group">
                <label>Common Ingredients:</label>
                {newRecipe.common_ingredients.map((ingredient, index) => (
                  <div key={index} className="common-ingredient-group">
                    <input
                      type="text"
                      placeholder="Common ingredient (salt, pepper, etc.)"
                      value={ingredient}
                      onChange={(e) => updateCommonIngredient(index, e.target.value)}
                      required
                    />
                    {newRecipe.common_ingredients.length > 1 && (
                      <button type="button" onClick={() => removeCommonIngredient(index)} className="remove-button">
                        Remove
                      </button>
                    )}
                  </div>
                ))}
                <button type="button" onClick={addCommonIngredient} className="add-ingredient-button">
                  Add Common Ingredient
                </button>
              </div>

              <div className="form-group">
                <label htmlFor="instructions">Instructions:</label>
                <textarea
                  id="instructions"
                  value={newRecipe.instructions}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, instructions: e.target.value }))}
                  rows={4}
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="prep_time">Prep Time (minutes):</label>
                  <input
                    type="number"
                    id="prep_time"
                    value={newRecipe.prep_time || ''}
                    onChange={(e) => setNewRecipe(prev => ({ ...prev, prep_time: parseInt(e.target.value) || 0 }))}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="portions">Portions:</label>
                  <input
                    type="number"
                    id="portions"
                    value={newRecipe.portions || ''}
                    onChange={(e) => setNewRecipe(prev => ({ ...prev, portions: parseInt(e.target.value) || 0 }))}
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={addingRecipe} className="submit-button">
                  {addingRecipe ? 'Adding Recipe...' : 'Add Recipe'}
                </button>
                <button type="button" onClick={() => setShowAddForm(false)} className="cancel-button">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Temporary debug info */}
        <div style={{backgroundColor: '#333', padding: '10px', margin: '10px', borderRadius: '5px', fontSize: '14px'}}>
          <p><strong>Debug Info:</strong></p>
          <p>Recipes array length: {recipes.length}</p>
          <p>Loading: {loading.toString()}</p>
          <p>Error: {error || 'none'}</p>
        </div>
        
        {recipes.length > 0 && (
          <div className="recipes">
            <h2>Recipes ({recipes.length})</h2>
            <div className="recipes-grid">
              {recipes.map((recipe) => (
                <div key={recipe.id} className="recipe-card">
                  <h3>{recipe.name}</h3>
                  <div className="recipe-details">
                    <p><strong>Category:</strong> {recipe.category}</p>
                    <p><strong>Prep Time:</strong> {recipe.prep_time} mins</p>
                    <p><strong>Portions:</strong> {recipe.portions}</p>
                  </div>
                  <div className="ingredients">
                    <h4>Main Ingredients:</h4>
                    <ul>
                      {recipe.main_ingredients.map((ingredient, index) => (
                        <li key={index}>
                          {ingredient.quantity} {ingredient.unit} {ingredient.name}
                        </li>
                      ))}
                    </ul>
                    <h4>Common Ingredients:</h4>
                    <ul>
                      {recipe.common_ingredients.map((ingredient, index) => (
                        <li key={index}>{ingredient}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="instructions">
                    <h4>Instructions:</h4>
                    <p>{recipe.instructions}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {recipes.length === 0 && !loading && !error && (
          <p>Click "Fetch Recipes" to load recipes from the backend.</p>
        )}
      </header>
    </div>
  );
}

export default App;