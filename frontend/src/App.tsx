import React, { useState } from 'react';
import './App.css';
import TopBar from './components/top-bar/TopBar';
import QuickActions from './components/quick-actions/QuickActions';
import Home from './pages/home/Home';

function App() {
  const [currentSection, setCurrentSection] = useState('Meal Planner');
  const [searchQuery, setSearchQuery] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleNavigation = (section: string) => {
    setCurrentSection(section);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleQuickAction = (action: string) => {
    setCurrentSection(action);
    setIsMobileMenuOpen(false); // Close mobile menu when action is selected
  };

  const handleMobileMenuToggle = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleCategoryClick = (category: string) => {
    setCurrentSection(category);
    setIsMobileMenuOpen(false); // Close mobile menu when category is selected
  };

  const handleRecipeClick = (recipe: any) => {
    setCurrentSection(`Recipe: ${recipe.name}`);
    setIsMobileMenuOpen(false); // Close mobile menu when recipe is selected
  };

  return (
    <div className="App">
      <TopBar
        currentUser={{ name: 'John Doe' }}
        onNavigate={handleNavigation}
        onSearch={handleSearch}
        onMenuToggle={handleMobileMenuToggle}
      />
      <QuickActions
        onActionClick={handleQuickAction}
        onCategoryClick={handleCategoryClick}
        onRecipeClick={handleRecipeClick}
        isMobileOpen={isMobileMenuOpen}
      />
      <main className="App-main">
        <div className="content-header">
          <h1>{currentSection}</h1>
        </div>

        <Home searchQuery={searchQuery} />
      </main>
    </div>
  );
}

export default App;
