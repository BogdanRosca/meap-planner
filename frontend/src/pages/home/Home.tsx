import React from 'react';
import './Home.css';

interface HomeProps {
  searchQuery: string;
}

const Home: React.FC<HomeProps> = ({ searchQuery }) => {
  return (
    <div className="home-content">
      {searchQuery && (
        <div className="search-results">
          <h3>Search Results for: "{searchQuery}"</h3>
          <p>Search functionality will be implemented here</p>
        </div>
      )}
    </div>
  );
};

export default Home;
