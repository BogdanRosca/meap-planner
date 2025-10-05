import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecentRecipes from './RecentRecipes';

describe('RecentRecipes', () => {
  const mockOnRecipeClick = jest.fn();

  beforeEach(() => {
    mockOnRecipeClick.mockClear();
  });

  it('renders recent recipes header', () => {
    render(<RecentRecipes />);
    expect(screen.getByText('Recent Recipes')).toBeInTheDocument();
  });

  it('renders all recent recipe items', () => {
    render(<RecentRecipes />);
    
    expect(screen.getByText('Açaí bowl')).toBeInTheDocument();
    expect(screen.getByText('Grilled Salmon')).toBeInTheDocument();
    expect(screen.getByText('Avocado Toast')).toBeInTheDocument();
    expect(screen.getByText('Chicken Salad')).toBeInTheDocument();
  });

  it('renders recipe categories', () => {
    render(<RecentRecipes />);
    
    expect(screen.getAllByText('Breakfast')).toHaveLength(2);
    expect(screen.getByText('Dinner')).toBeInTheDocument();
    expect(screen.getByText('Lunch')).toBeInTheDocument();
  });

  it('renders recipe images (emojis)', () => {
    render(<RecentRecipes />);
    
    expect(screen.getByText('🍓')).toBeInTheDocument();
    expect(screen.getByText('🍣')).toBeInTheDocument();
    expect(screen.getByText('🥑')).toBeInTheDocument();
    expect(screen.getByText('🥗')).toBeInTheDocument();
  });

  it('calls onRecipeClick when a recent recipe is clicked', () => {
    render(<RecentRecipes onRecipeClick={mockOnRecipeClick} />);
    
    const acaiBowlButton = screen.getByRole('button', { name: /açaí bowl/i });
    fireEvent.click(acaiBowlButton);
    
    expect(mockOnRecipeClick).toHaveBeenCalledWith({
      id: 'acai-bowl',
      name: 'Açaí bowl',
      category: 'Breakfast',
      image: '🍓'
    });
  });

  it('handles multiple recipe clicks correctly', () => {
    render(<RecentRecipes onRecipeClick={mockOnRecipeClick} />);
    
    const acaiBowlButton = screen.getByRole('button', { name: /açaí bowl/i });
    const salmonButton = screen.getByRole('button', { name: /grilled salmon/i });
    
    fireEvent.click(acaiBowlButton);
    fireEvent.click(salmonButton);
    
    expect(mockOnRecipeClick).toHaveBeenCalledTimes(2);
    expect(mockOnRecipeClick).toHaveBeenNthCalledWith(1, expect.objectContaining({
      name: 'Açaí bowl'
    }));
    expect(mockOnRecipeClick).toHaveBeenNthCalledWith(2, expect.objectContaining({
      name: 'Grilled Salmon'
    }));
  });

  it('works without onRecipeClick prop', () => {
    render(<RecentRecipes />);
    
    const acaiBowlButton = screen.getByRole('button', { name: /açaí bowl/i });
    
    expect(() => {
      fireEvent.click(acaiBowlButton);
    }).not.toThrow();
  });

  it('applies correct CSS classes', () => {
    render(<RecentRecipes />);
    
    expect(screen.getByRole('heading', { name: 'Recent Recipes' }).parentElement).toHaveClass('recent-recipes-header');
    
    const recipeButtons = screen.getAllByRole('button');
    recipeButtons.forEach(button => {
      expect(button).toHaveClass('recent-recipe-item');
    });
  });

  it('has proper structure for recipe items', () => {
    render(<RecentRecipes />);
    
    const acaiBowlButton = screen.getByRole('button', { name: /açaí bowl/i });
    
    // Check for image container
    expect(acaiBowlButton.querySelector('.recipe-image')).toBeInTheDocument();
    expect(acaiBowlButton.querySelector('.recipe-image')).toHaveTextContent('🍓');
    
    // Check for info container
    expect(acaiBowlButton.querySelector('.recipe-info')).toBeInTheDocument();
    expect(acaiBowlButton.querySelector('.recipe-name')).toHaveTextContent('Açaí bowl');
    expect(acaiBowlButton.querySelector('.recipe-category')).toHaveTextContent('Breakfast');
  });

});