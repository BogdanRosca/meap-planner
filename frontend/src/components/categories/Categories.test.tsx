import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Categories from './Categories';

describe('Categories Component', () => {
  const mockOnCategoryClick = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the Categories component with title', () => {
    render(<Categories />);

    expect(screen.getByText('Categories')).toBeInTheDocument();
  });

  it('renders all category items', () => {
    render(<Categories />);

    expect(screen.getByText('Breakfast')).toBeInTheDocument();
    expect(screen.getByText('Snack')).toBeInTheDocument();
    expect(screen.getByText('Lunch')).toBeInTheDocument();
    expect(screen.getByText('Dinner')).toBeInTheDocument();
  });

  it('renders category icons', () => {
    const { container } = render(<Categories />);

    const icons = container.querySelectorAll('.category-icon');
    expect(icons).toHaveLength(4);

    // Check for specific icons
    expect(container.textContent).toContain('☕️'); // Breakfast and Lunch
    expect(container.textContent).toContain('🍎'); // Snack
    expect(container.textContent).toContain('🌙'); // Dinner
  });

  it('renders category counts with correct values', () => {
    render(<Categories />);

    // Check for count badges
    expect(screen.getByText('6')).toBeInTheDocument(); // Breakfast
    expect(screen.getByText('2')).toBeInTheDocument(); // Snack

    // Get all elements with text '1' to check both Lunch and Dinner
    const oneCount = screen.getAllByText('1');
    expect(oneCount).toHaveLength(2); // Lunch and Dinner both have count 1
  });

  it('calls onCategoryClick when a category is clicked', () => {
    render(<Categories onCategoryClick={mockOnCategoryClick} />);

    const breakfastButton = screen.getByText('Breakfast').closest('button');
    fireEvent.click(breakfastButton!);

    expect(mockOnCategoryClick).toHaveBeenCalledWith('Breakfast');
    expect(mockOnCategoryClick).toHaveBeenCalledTimes(1);
  });

  it('calls onCategoryClick for all category buttons', () => {
    render(<Categories onCategoryClick={mockOnCategoryClick} />);

    const breakfastButton = screen.getByText('Breakfast').closest('button');
    const snackButton = screen.getByText('Snack').closest('button');
    const lunchButton = screen.getByText('Lunch').closest('button');
    const dinnerButton = screen.getByText('Dinner').closest('button');

    fireEvent.click(breakfastButton!);
    fireEvent.click(snackButton!);
    fireEvent.click(lunchButton!);
    fireEvent.click(dinnerButton!);

    expect(mockOnCategoryClick).toHaveBeenNthCalledWith(1, 'Breakfast');
    expect(mockOnCategoryClick).toHaveBeenNthCalledWith(2, 'Snack');
    expect(mockOnCategoryClick).toHaveBeenNthCalledWith(3, 'Lunch');
    expect(mockOnCategoryClick).toHaveBeenNthCalledWith(4, 'Dinner');
    expect(mockOnCategoryClick).toHaveBeenCalledTimes(4);
  });

  it('applies correct CSS custom properties for category colors', () => {
    const { container } = render(<Categories />);

    const categoryButtons = container.querySelectorAll('.category-item');
    expect(categoryButtons).toHaveLength(4);

    // Check that category buttons have style attribute with --category-color
    const breakfastButton = screen
      .getByText('Breakfast')
      .closest('button') as HTMLElement;
    const snackButton = screen
      .getByText('Snack')
      .closest('button') as HTMLElement;
    const lunchButton = screen
      .getByText('Lunch')
      .closest('button') as HTMLElement;
    const dinnerButton = screen
      .getByText('Dinner')
      .closest('button') as HTMLElement;

    expect(breakfastButton.style.getPropertyValue('--category-color')).toBe(
      '#5b8266'
    );
    expect(snackButton.style.getPropertyValue('--category-color')).toBe(
      '#294936'
    );
    expect(lunchButton.style.getPropertyValue('--category-color')).toBe(
      '#3e6259'
    );
    expect(dinnerButton.style.getPropertyValue('--category-color')).toBe(
      '#212922'
    );
  });

  it('has proper category structure with content and count', () => {
    const { container } = render(<Categories />);

    const categoryItems = container.querySelectorAll('.category-item');
    categoryItems.forEach(item => {
      expect(item.querySelector('.category-content')).toBeInTheDocument();
      expect(item.querySelector('.category-icon')).toBeInTheDocument();
      expect(item.querySelector('.category-name')).toBeInTheDocument();
      expect(item.querySelector('.category-count')).toBeInTheDocument();
    });
  });

  it('has proper accessibility attributes', () => {
    render(<Categories />);

    const categoryButtons = screen.getAllByRole('button');
    // Should have 4 category buttons
    const categorySpecificButtons = categoryButtons.filter(
      button =>
        button.textContent?.includes('Breakfast') ||
        button.textContent?.includes('Snack') ||
        button.textContent?.includes('Lunch') ||
        button.textContent?.includes('Dinner')
    );

    expect(categorySpecificButtons).toHaveLength(4);

    categorySpecificButtons.forEach((button: HTMLElement) => {
      expect(button).toBeInTheDocument();
      expect(button.tagName).toBe('BUTTON');
    });
  });

  it('works without onCategoryClick prop', () => {
    render(<Categories />);

    const breakfastButton = screen.getByText('Breakfast').closest('button');

    // Should not throw error when clicked without callback
    expect(() => {
      fireEvent.click(breakfastButton!);
    }).not.toThrow();
  });

  it('renders categories in correct order', () => {
    render(<Categories />);

    const categoryNames = screen.getAllByText(
      /^(Breakfast|Snack|Lunch|Dinner)$/
    );
    const expectedOrder = ['Breakfast', 'Snack', 'Lunch', 'Dinner'];

    categoryNames.forEach((element, index) => {
      expect(element.textContent).toBe(expectedOrder[index]);
    });
  });

  it('has correct category data structure', () => {
    render(<Categories />);

    // Test that each category has the expected structure
    const breakfastCategory = screen
      .getByText('Breakfast')
      .closest('.category-item');
    const snackCategory = screen.getByText('Snack').closest('.category-item');
    const lunchCategory = screen.getByText('Lunch').closest('.category-item');
    const dinnerCategory = screen.getByText('Dinner').closest('.category-item');

    expect(breakfastCategory).toContainElement(screen.getByText('6'));
    expect(snackCategory).toContainElement(screen.getByText('2'));

    // For the categories with count 1, we need to be more specific
    const lunchCount = lunchCategory?.querySelector('.category-count');
    const dinnerCount = dinnerCategory?.querySelector('.category-count');

    expect(lunchCount?.textContent).toBe('1');
    expect(dinnerCount?.textContent).toBe('1');
  });
});
