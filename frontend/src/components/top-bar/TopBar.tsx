import React, { useState } from 'react';
import './TopBar.css';

interface TopBarProps {
  currentUser?: {
    name: string;
    avatar?: string;
  };
  onNavigate?: (section: string) => void;
  onSearch?: (query: string) => void;
  onMenuToggle?: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ 
  currentUser = { name: 'John Doe' }, 
  onNavigate,
  onSearch,
  onMenuToggle 
}) => {
  const [activeTab, setActiveTab] = useState('Meal Planner');
  const [searchQuery, setSearchQuery] = useState('');

  const navigationItems = [
    'Meal Planner',
    'Recipes', 
    'Shopping List',
    'Analytics'
  ];

  const handleNavClick = (item: string) => {
    setActiveTab(item);
    onNavigate?.(item);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    onSearch?.(query);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchQuery);
  };

  return (
    <header className="top-bar">
      <div className="top-bar-container">
        {/* Mobile Menu Button */}
        <button className="mobile-menu-btn" onClick={onMenuToggle}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>

        {/* Logo Section */}
        <div className="logo-section">
          <div className="logo-icon">🍴</div>
          <span className="logo-text">MealCraft</span>
        </div>

        {/* Navigation Section */}
        <nav className="navigation">
          {navigationItems.map((item) => (
            <button
              key={item}
              className={`nav-item ${activeTab === item ? 'active' : ''}`}
              onClick={() => handleNavClick(item)}
            >
              {item}
            </button>
          ))}
        </nav>

        {/* Search Section */}
        <div className="search-section">
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
                <svg 
                  width="16" 
                  height="16" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="21 21l-4.35-4.35" />
                </svg>
              </button>
            </div>
          </form>
        </div>

        {/* User Section */}
        <div className="user-section">
          <div className="language-selector">
            <span className="flag">🇺🇸</span>
          </div>
          <div className="user-profile">
            <div className="user-avatar">
              {currentUser.avatar ? (
                <img src={currentUser.avatar} alt={currentUser.name} />
              ) : (
                <div className="avatar-placeholder">
                  {currentUser.name.split(' ').map(n => n[0]).join('')}
                </div>
              )}
            </div>
            <span className="user-name">{currentUser.name}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default TopBar;