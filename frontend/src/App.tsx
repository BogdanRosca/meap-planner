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
