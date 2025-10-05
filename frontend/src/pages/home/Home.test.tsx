import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from './Home';

describe('Home Component', () => {
  test('renders search results when search query is provided', () => {
    const searchQuery = 'chicken';
    render(<Home searchQuery={searchQuery} />);

    expect(
      screen.getByText(`Search Results for: "${searchQuery}"`)
    ).toBeInTheDocument();
    expect(
      screen.getByText('Search functionality will be implemented here')
    ).toBeInTheDocument();
  });

  test('does not render welcome section when search query is provided', () => {
    render(<Home searchQuery="chicken" />);

    expect(
      screen.queryByText('Welcome to Meal Planner')
    ).not.toBeInTheDocument();
    expect(screen.queryByText('Plan Meals')).not.toBeInTheDocument();
  });
});
