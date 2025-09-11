# Meal Planner API

A simple FastAPI backend service for a meal planning application.

## Features

- Health check endpoint
- Built with FastAPI
- Unit tests with pytest

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

4. Visit the API:
   - Health endpoint: http://127.0.0.1:8000/health
   - Interactive docs: http://127.0.0.1:8000/docs

## Testing

Run the tests with:
```bash
pytest test_main.py -v
```

## API Endpoints

### GET /health
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "message": "Meal Planner API is running!"
}
```
