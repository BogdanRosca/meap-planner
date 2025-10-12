import React, { useState, useEffect } from 'react';
import './Recipes.css';
import { Recipe } from '../../types/recipe';
import { recipeService } from '../../services/recipeService';
import RecipeDetailModal from '../../components/recipe/RecipeDetailModal';
import AddRecipeModal from '../../components/recipe/AddRecipeModal';
import ConfirmationPopup from '../../components/popup/ConfirmationPopup';

interface RecipesProps {
  searchQuery?: string;
}

const Recipes: React.FC<RecipesProps> = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [isAddRecipeModalOpen, setIsAddRecipeModalOpen] =
    useState<boolean>(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState<{
    isOpen: boolean;
    recipeId: number | null;
    recipeName: string;
  }>({
    isOpen: false,
    recipeId: null,
    recipeName: '',
  });

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await recipeService.getAllRecipes();
        setRecipes(data);
      } catch (err) {
        setError('Failed to load recipes. Please try again later.');
        console.error('Error loading recipes:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  // Filter recipes based on search query
  const filteredRecipes = searchQuery
    ? recipes.filter(recipe =>
        recipe.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : recipes;

  // Category emoji mapping
  const getCategoryEmoji = (category: string): string => {
    const emojiMap: { [key: string]: string } = {
      breakfast: '🍳',
      lunch: '🥗',
      dinner: '🍽️',
      snack: '🍿',
    };
    return emojiMap[category.toLowerCase()] || '🍴';
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
  };

  const handleRecipeClick = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedRecipe(null);
  };

  const handleOpenAddRecipeModal = () => {
    setIsAddRecipeModalOpen(true);
  };

  const handleCloseAddRecipeModal = () => {
    setIsAddRecipeModalOpen(false);
  };

  const handleDeleteClick = (e: React.MouseEvent, recipe: Recipe) => {
    e.stopPropagation();
    setDeleteConfirmation({
      isOpen: true,
      recipeId: recipe.id,
      recipeName: recipe.name,
    });
  };

  const handleCancelDelete = () => {
    setDeleteConfirmation({
      isOpen: false,
      recipeId: null,
      recipeName: '',
    });
  };

  const handleConfirmDelete = async () => {
    if (deleteConfirmation.recipeId) {
      try {
        await recipeService.deleteRecipe(deleteConfirmation.recipeId);
        setRecipes(
          recipes.filter(recipe => recipe.id !== deleteConfirmation.recipeId)
        );
        handleCancelDelete(); // Close the confirmation popup
      } catch (err) {
        console.error('Error deleting recipe:', err);
        // You could set an error state here to show an error message
      }
    }
  };

  const handleAddRecipe = async (newRecipe: Omit<Recipe, 'id'>) => {
    try {
      const addedRecipe = await recipeService.addRecipe(newRecipe);
      setRecipes([...recipes, addedRecipe]);
      handleCloseAddRecipeModal();
    } catch (err) {
      console.error('Error adding recipe:', err);
      // You could set an error state here to show an error message
    }
  };

  if (loading) {
    return (
      <div className="recipes-content">
        <div className="loading-message">Loading recipes...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recipes-content">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="recipes-content">
      {/* Search and Action Section */}
      <div className="recipes-action-bar">
        <div className="recipes-search-section">
          <form onSubmit={handleSearchSubmit} className="search-form">
            <div className="search-input-container">
              <input
                type="text"
                placeholder="Search recipes..."
                value={searchQuery}
                onChange={handleSearchChange}
                className="search-input"
              />
              <button type="submit" className="search-button">
                <img
                  width="16px"
                  src="assets/search.png"
                  alt="Search"
                  className="search-icon"
                />
              </button>
            </div>
          </form>
        </div>
        <button
          className="add-recipe-button"
          onClick={handleOpenAddRecipeModal}
        >
          + Add recipe
        </button>
      </div>

      {filteredRecipes.length === 0 ? (
        <div className="no-recipes-message">
          {searchQuery
            ? 'No recipes found matching your search.'
            : 'No recipes available yet.'}
        </div>
      ) : (
        <div className="recipes-grid">
          {filteredRecipes.map(recipe => (
            <div key={recipe.id} className="recipe-card">
              <div
                className="recipe-card-main"
                onClick={() => handleRecipeClick(recipe)}
              >
                <div className="recipe-card-image">
                  <div className="recipe-placeholder">
                    {getCategoryEmoji(recipe.category)}
                  </div>
                </div>
                <div className="recipe-card-content">
                  <div className="recipe-title-container">
                    <h3 className="recipe-card-title">{recipe.name}</h3>
                    <div
                      className="recipe-delete-button"
                      onClick={e => handleDeleteClick(e, recipe)}
                    >
                      <img
                        src="assets/delete.png"
                        alt="Delete"
                        className="delete-icon"
                      />
                    </div>
                  </div>
                  <div
                    className={`recipe-category-badge category-${recipe.category.toLowerCase()}`}
                  >
                    {recipe.category}
                  </div>
                  <div className="recipe-card-footer">
                    <span className="recipe-time">
                      ⏱️ {recipe.prep_time} min
                    </span>
                    <span className="recipe-portions">
                      👥 {recipe.portions}{' '}
                      {recipe.portions === 1 ? 'portion' : 'portions'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Recipe Detail Modal */}
      {selectedRecipe && (
        <RecipeDetailModal
          recipe={selectedRecipe}
          isOpen={isModalOpen}
          onClose={handleCloseModal}
        />
      )}

      {/* Add Recipe Modal */}
      <AddRecipeModal
        isOpen={isAddRecipeModalOpen}
        onClose={handleCloseAddRecipeModal}
        onAddRecipe={handleAddRecipe}
      />

      {/* Delete Confirmation Popup */}
      <ConfirmationPopup
        isOpen={deleteConfirmation.isOpen}
        title="Delete Recipe"
        message={`Are you sure you want to delete "${deleteConfirmation.recipeName}"?`}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
      />
    </div>
  );
};

export default Recipes;
