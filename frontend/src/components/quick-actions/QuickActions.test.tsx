import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import QuickActions from './QuickActions';

describe('QuickActions Component', () => {
  const mockOnActionClick = jest.fn();
  const mockOnCategoryClick = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the QuickActions component with title', () => {
    render(<QuickActions />);

    expect(screen.getByText('Quick Actions')).toBeInTheDocument();
  });

  it('renders all quick action items', () => {
    render(<QuickActions />);

    expect(screen.getByText('Add Recipe')).toBeInTheDocument();
    expect(screen.getByText('Plan Meals')).toBeInTheDocument();
    expect(screen.getByText('Shopping List')).toBeInTheDocument();

    expect(screen.getByText('Create a new recipe')).toBeInTheDocument();
    expect(screen.getByText('Plan your weekly meals')).toBeInTheDocument();
    expect(screen.getByText('Create shopping list')).toBeInTheDocument();
  });

  it('renders action icons', () => {
    render(<QuickActions />);

    const actionButtons = screen.getAllByRole('button');
    // Filter out category buttons by checking for quick action specific content
    const quickActionButtons = actionButtons.filter(
      (button: HTMLElement) =>
        button.textContent?.includes('Create') ||
        button.textContent?.includes('Plan your weekly')
    );

    expect(quickActionButtons).toHaveLength(3);
  });

  it('calls onActionClick when a quick action is clicked', () => {
    render(<QuickActions onActionClick={mockOnActionClick} />);

    const addRecipeButton = screen.getByText('Add Recipe').closest('button');
    fireEvent.click(addRecipeButton!);

    expect(mockOnActionClick).toHaveBeenCalledWith('Add Recipe');
    expect(mockOnActionClick).toHaveBeenCalledTimes(1);
  });

  it('calls onActionClick for all quick action buttons', () => {
    render(<QuickActions onActionClick={mockOnActionClick} />);

    const addRecipeButton = screen.getByText('Add Recipe').closest('button');
    const planMealsButton = screen.getByText('Plan Meals').closest('button');
    const shoppingListButton = screen
      .getByText('Shopping List')
      .closest('button');

    fireEvent.click(addRecipeButton!);
    fireEvent.click(planMealsButton!);
    fireEvent.click(shoppingListButton!);

    expect(mockOnActionClick).toHaveBeenNthCalledWith(1, 'Add Recipe');
    expect(mockOnActionClick).toHaveBeenNthCalledWith(2, 'Plan Meals');
    expect(mockOnActionClick).toHaveBeenNthCalledWith(3, 'Shopping List');
    expect(mockOnActionClick).toHaveBeenCalledTimes(3);
  });

  it('applies mobile-open class when isMobileOpen is true', () => {
    const { container } = render(<QuickActions isMobileOpen={true} />);

    const quickActionsAside = container.querySelector('.quick-actions');
    expect(quickActionsAside).toHaveClass('mobile-open');
  });

  it('does not apply mobile-open class when isMobileOpen is false', () => {
    const { container } = render(<QuickActions isMobileOpen={false} />);

    const quickActionsAside = container.querySelector('.quick-actions');
    expect(quickActionsAside).not.toHaveClass('mobile-open');
  });

  it('renders Categories component within QuickActions', () => {
    render(<QuickActions />);

    // Check that Categories component is rendered
    expect(screen.getByText('Categories')).toBeInTheDocument();
    // Use getAllByText to handle multiple elements with same text
    expect(screen.getAllByText('Breakfast')).toHaveLength(3); // One in categories, two in recent recipes
    expect(screen.getAllByText('Lunch')).toHaveLength(2); // One in categories, one in recent recipes
    expect(screen.getAllByText('Dinner')).toHaveLength(2); // One in categories, one in recent recipes
    expect(screen.getByText('Snack')).toBeInTheDocument(); // Only appears in categories
  });

  it('calls onCategoryClick when a category is clicked', () => {
    render(<QuickActions onCategoryClick={mockOnCategoryClick} />);

    // Find the category button specifically (the one with category-item class)
    const categorySection = screen
      .getByText('Categories')
      .closest('.categories-section');
    const breakfastButton = categorySection?.querySelector('.category-item');
    expect(breakfastButton).toBeTruthy();
    fireEvent.click(breakfastButton!);

    expect(mockOnCategoryClick).toHaveBeenCalledWith('Breakfast');
    expect(mockOnCategoryClick).toHaveBeenCalledTimes(1);
  });

  it('has proper accessibility attributes', () => {
    render(<QuickActions />);

    const quickActionsSection = screen.getByRole('complementary');
    expect(quickActionsSection).toBeInTheDocument();

    const actionButtons = screen.getAllByRole('button');
    actionButtons.forEach((button: HTMLElement) => {
      expect(button).toBeInTheDocument();
    });
  });

  it('renders arrow indicators for each action', () => {
    const { container } = render(<QuickActions />);

    const arrows = container.querySelectorAll('.action-arrow');
    // Should have 3 arrows for quick actions (categories have their own component)
    const quickActionArrows = Array.from(arrows).filter(
      (arrow: Element) => arrow.textContent === '→'
    );
    expect(quickActionArrows.length).toBeGreaterThanOrEqual(3);
  });
});
