-- Database initialization script for Meal Planner
-- Creates the recipes table with the required schema

CREATE TABLE IF NOT EXISTS recipes (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(20) CHECK (category IN ('breakfast', 'lunch', 'dinner', 'snack')),
  main_ingredients JSONB,
  common_ingredients TEXT[] DEFAULT '{}',
  instructions TEXT NOT NULL,
  prep_time INTEGER,
  portions INTEGER
);

-- Insert a sample recipe for testing
INSERT INTO recipes (name, category, main_ingredients, common_ingredients, instructions, prep_time, portions) 
VALUES (
  'Sample Pasta Recipe', 
  'dinner', 
  '[
    {"name": "pasta", "unit": "g", "quantity": 250},
    {"name": "tomato", "unit": "g", "quantity": 500},
    {"name": "onion", "unit": "pcs", "quantity": 1},
    {"name": "burrata", "unit": "pcs", "quantity": 1}
  ]'::jsonb,
  ARRAY['salt', 'pepper', 'basil', 'olive oil', 'garlic'],
  'Cook pasta according to package instructions. In a pan, sauté diced onion with olive oil and garlic. Add tomatoes and seasonings. Combine with pasta and top with burrata.',
  30,
  2
) ON CONFLICT DO NOTHING;