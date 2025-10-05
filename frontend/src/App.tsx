import React, { useState } from 'react';
import './App.css';
import TopBar from './components/TopBar';
import QuickActions from './components/QuickActions';

function App() {
  const [currentSection, setCurrentSection] = useState('Meal Planner');
  const [searchQuery, setSearchQuery] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleNavigation = (section: string) => {
    setCurrentSection(section);
    console.log(`Navigating to: ${section}`);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    console.log(`Searching for: ${query}`);
  };

  const handleQuickAction = (action: string) => {
    setCurrentSection(action);
    setIsMobileMenuOpen(false); // Close mobile menu when action is selected
    console.log(`Quick action: ${action}`);
  };

  const handleMobileMenuToggle = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleCategoryClick = (category: string) => {
    setCurrentSection(category);
    setIsMobileMenuOpen(false); // Close mobile menu when category is selected
    console.log(`Category selected: ${category}`);
  };

  return (
    <div className="App">
      <TopBar 
        currentUser={{ name: 'Bogdan Rosca' }}
        onNavigate={handleNavigation}
        onSearch={handleSearch}
        onMenuToggle={handleMobileMenuToggle}
      />
      <QuickActions 
        onActionClick={handleQuickAction}
        onCategoryClick={handleCategoryClick}
        isMobileOpen={isMobileMenuOpen}
      />
      <main className="App-main">
        <div className="content-header">
          <h1>{currentSection}</h1>
        </div>

        <div className="home-content">
          <div className="welcome-section">
            <h2>Welcome to MealCraft</h2>
            <p>Your personal meal planning companion</p>
          </div>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📝</div>
              <h3>Meal Planner</h3>
              <p>Plan your meals for the week and stay organized</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🍳</div>
              <h3>Recipes</h3>
              <p>Discover and save your favorite recipes</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🛒</div>
              <h3>Shopping List</h3>
              <p>Generate shopping lists from your meal plans</p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Analytics</h3>
              <p>Track your meal planning habits and preferences</p>
            </div>
          </div>

          {searchQuery && (
            <div className="search-results">
              <h3>Search Results for: "{searchQuery}"</h3>
              <p>Search functionality will be implemented here</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
