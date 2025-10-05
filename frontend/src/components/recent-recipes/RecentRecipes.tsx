import React from 'react';
import './RecentRecipes.css';

interface Recipe {
  id: string;
  name: string;
  category: string;
  image: string;
}

interface RecentRecipesProps {
  onRecipeClick?: (_recipe: Recipe) => void;
}

const RecentRecipes: React.FC<RecentRecipesProps> = ({ onRecipeClick }) => {
  const recentRecipes: Recipe[] = [
    {
      id: 'acai-bowl',
      name: 'Açaí bowl',
      category: 'Breakfast',
      image: '🍓',
    },
    {
      id: 'grilled-salmon',
      name: 'Grilled Salmon',
      category: 'Dinner',
      image: '🍣',
    },
    {
      id: 'avocado-toast',
      name: 'Avocado Toast',
      category: 'Breakfast',
      image: '🥑',
    },
    {
      id: 'chicken-salad',
      name: 'Chicken Salad',
      category: 'Lunch',
      image: '🥗',
    },
  ];

  const handleRecipeClick = (recipe: Recipe) => {
    onRecipeClick?.(recipe);
  };

  return (
    <div className="recent-recipes-section">
      <div className="recent-recipes-header">
        <h3>Recent Recipes</h3>
      </div>
      <div className="recent-recipes-list">
        {recentRecipes.map(recipe => (
          <button
            key={recipe.id}
            className="recent-recipe-item"
            onClick={() => handleRecipeClick(recipe)}
          >
            <div className="recipe-image">{recipe.image}</div>
            <div className="recipe-info">
              <h4 className="recipe-name">{recipe.name}</h4>
              <p className="recipe-category">{recipe.category}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default RecentRecipes;
