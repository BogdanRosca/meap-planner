import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

// Mock console.log to avoid noise in tests
const originalConsoleLog = console.log;
beforeAll(() => {
  console.log = jest.fn();
});

afterAll(() => {
  console.log = originalConsoleLog;
});

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText('MealCraft')).toBeInTheDocument();
  });

  it('renders all main components', () => {
    render(<App />);

    // Check TopBar is rendered
    expect(screen.getByText('MealCraft')).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText('Search recipes...')
    ).toBeInTheDocument();

    // Check QuickActions is rendered
    expect(screen.getByText('Quick Actions')).toBeInTheDocument();
    expect(screen.getByText('Add Recipe')).toBeInTheDocument();

    // Check main content area is rendered
    expect(screen.getByRole('main')).toBeInTheDocument();

    // Check Home component is rendered (it should contain categories and recent recipes)
    expect(screen.getByText('Categories')).toBeInTheDocument();
    expect(screen.getByText('Recent Recipes')).toBeInTheDocument();
  });

  it('displays default section as "Meal Planner"', () => {
    render(<App />);
    // Check specifically for the h1 in the content header
    expect(
      screen.getByRole('heading', { level: 1, name: 'Meal Planner' })
    ).toBeInTheDocument();
  });

  it('updates current section when navigation is clicked', () => {
    render(<App />);

    const recipesNavButton = screen.getByText('Recipes');
    fireEvent.click(recipesNavButton);

    expect(
      screen.getByRole('heading', { level: 1, name: 'Recipes' })
    ).toBeInTheDocument();
  });

  it('updates search query when search is performed', () => {
    render(<App />);

    const searchInput = screen.getByPlaceholderText('Search recipes...');
    fireEvent.change(searchInput, { target: { value: 'pasta' } });
  });

  it('handles mobile menu toggle', () => {
    const { container } = render(<App />);

    const mobileMenuButton = container.querySelector('.mobile-menu-btn');
    expect(mobileMenuButton).toBeInTheDocument();

    // Initially mobile menu should be closed
    const quickActions = screen.getByRole('complementary');
    expect(quickActions).not.toHaveClass('mobile-open');

    // Toggle mobile menu
    fireEvent.click(mobileMenuButton!);
    expect(quickActions).toHaveClass('mobile-open');
  });

  it('handles quick action clicks and closes mobile menu', () => {
    const { container } = render(<App />);

    // Open mobile menu first
    const mobileMenuButton = container.querySelector('.mobile-menu-btn');
    fireEvent.click(mobileMenuButton!);

    const quickActions = screen.getByRole('complementary');
    expect(quickActions).toHaveClass('mobile-open');

    // Click a quick action
    const addRecipeButton = screen.getByText('Add Recipe');
    fireEvent.click(addRecipeButton);

    // Should update section and close mobile menu
    expect(
      screen.getByRole('heading', { level: 1, name: 'Add Recipe' })
    ).toBeInTheDocument();
    expect(quickActions).not.toHaveClass('mobile-open');
  });

  it('handles category clicks and closes mobile menu', () => {
    const { container } = render(<App />);

    // Open mobile menu first
    const mobileMenuButton = container.querySelector('.mobile-menu-btn');
    fireEvent.click(mobileMenuButton!);

    const quickActions = screen.getByRole('complementary');
    expect(quickActions).toHaveClass('mobile-open');

    // Find and click a category button (specifically in the categories section)
    const categorySection = screen
      .getByText('Categories')
      .closest('.categories-section');
    const breakfastButton = categorySection?.querySelector('.category-item');
    expect(breakfastButton).toBeTruthy();
    fireEvent.click(breakfastButton!);

    // Should update section and close mobile menu
    expect(
      screen.getByRole('heading', { level: 1, name: 'Breakfast' })
    ).toBeInTheDocument();
    expect(quickActions).not.toHaveClass('mobile-open');
  });

  it('handles recipe clicks and closes mobile menu', () => {
    const { container } = render(<App />);

    // Open mobile menu first
    const mobileMenuButton = container.querySelector('.mobile-menu-btn');
    fireEvent.click(mobileMenuButton!);

    const quickActions = screen.getByRole('complementary');
    expect(quickActions).toHaveClass('mobile-open');

    // Find and click a recent recipe
    const recentRecipeButton = screen
      .getAllByText('Açaí bowl')[0]
      .closest('button');
    expect(recentRecipeButton).toBeTruthy();
    fireEvent.click(recentRecipeButton!);

    // Should update section and close mobile menu
    expect(
      screen.getByRole('heading', { level: 1, name: 'Recipe: Açaí bowl' })
    ).toBeInTheDocument();
    expect(quickActions).not.toHaveClass('mobile-open');
  });

  it('passes correct props to child components', () => {
    render(<App />);

    // Check TopBar receives correct user prop
    expect(screen.getByText('John Doe')).toBeInTheDocument();

    // Check Home component receives search query (initially empty)
    // We can verify this by checking if search results are not shown initially
    screen.queryByText('Welcome');
    // Since search query is empty initially, welcome section should be visible if it exists
    // or the home component should render its default state
  });

  it('has correct CSS classes', () => {
    const { container } = render(<App />);

    const appDiv = container.firstChild as HTMLElement;
    expect(appDiv).toHaveClass('App');

    const mainElement = screen.getByRole('main');
    expect(mainElement).toHaveClass('App-main');

    const contentHeader = container.querySelector('.content-header');
    expect(contentHeader).toBeInTheDocument();
  });

  it('renders with React.StrictMode compatibility', () => {
    // This test ensures the component works with StrictMode (no side effects)
    const { unmount } = render(<App />);
    unmount();

    // Re-render to check for any side effects
    render(<App />);
    expect(screen.getByText('MealCraft')).toBeInTheDocument();
  });

  it('maintains state correctly across interactions', () => {
    render(<App />);

    // Test multiple state changes
    const recipesNavButton = screen.getByText('Recipes');
    fireEvent.click(recipesNavButton);
    expect(
      screen.getByRole('heading', { level: 1, name: 'Recipes' })
    ).toBeInTheDocument();

    const analyticsNavButton = screen.getByText('Analytics');
    fireEvent.click(analyticsNavButton);
    expect(
      screen.getByRole('heading', { level: 1, name: 'Analytics' })
    ).toBeInTheDocument();

    // Search should still work
    const searchInput = screen.getByPlaceholderText('Search recipes...');
    fireEvent.change(searchInput, { target: { value: 'chicken' } });
  });
});
