import React from 'react';
import './QuickActions.css';
import Categories from '../categories/Categories';
import RecentRecipes from '../recent-recipes/RecentRecipes';

interface QuickActionsProps {
  onActionClick?: (action: string) => void;
  onCategoryClick?: (category: string) => void;
  onRecipeClick?: (recipe: any) => void;
  isMobileOpen?: boolean;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onActionClick, onCategoryClick, onRecipeClick, isMobileOpen = false }) => {
  const actions = [
    {
      id: 'add-recipe',
      title: 'Add Recipe',
      icon: '🍳',
      description: 'Create a new recipe'
    },
    {
      id: 'plan-meals',
      title: 'Plan Meals',
      icon: '📅',
      description: 'Plan your weekly meals'
    },
    {
      id: 'shopping-list',
      title: 'Shopping List',
      icon: '🛒',
      description: 'Create shopping list'
    }
  ];

  const handleActionClick = (actionId: string, actionTitle: string) => {
    onActionClick?.(actionTitle);
    console.log(`Quick action clicked: ${actionTitle}`);
  };

  return (
    <aside className={`quick-actions ${isMobileOpen ? 'mobile-open' : ''}`}>
      <div className="quick-actions-header">
        <h3>Quick Actions</h3>
      </div>
      <div className="quick-actions-list">
        {actions.map((action) => (
          <button
            key={action.id}
            className="quick-action-item"
            onClick={() => handleActionClick(action.id, action.title)}
          >
            <div className="action-icon">{action.icon}</div>
            <div className="action-content">
              <h4>{action.title}</h4>
              <p>{action.description}</p>
            </div>
            <div className="action-arrow">→</div>
          </button>
        ))}
      </div>
      
      {/* Categories Section */}
      <Categories onCategoryClick={onCategoryClick} />
      
      {/* Recent Recipes Section */}
      <RecentRecipes onRecipeClick={onRecipeClick} />
    </aside>
  );
};

export default QuickActions;