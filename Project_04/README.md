# NASA Moon Middleware API

A FastAPI middleware that fetches moon-related data from NASA's public APIs (Image Library & APOD) and returns structured JSON.

## Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns the service status.
- **Response:**
  ```json
  { "service": "NASA Moon Middleware", "status": "running" }
  ```

### 2. Search Moon Images

- **URL:** `/moon/images`
- **Method:** `GET`
- **Description:** Searches NASA's Image Library for moon-related photos.
- **Query Parameters:**
  - `q` (String, default: `"moon"`): Search query.
  - `limit` (Integer, default: `5`, max: `50`): Number of results to return.
- **Response:**
  ```json
  {
    "query": "moon",
    "count": 5,
    "results": [
      {
        "title": "Nearside of the Moon",
        "description": "Nearside of the Moon",
        "date_created": "2009-09-24T18:00:22Z",
        "nasa_id": "PIA12235",
        "image_url": "https://images-assets.nasa.gov/image/PIA12235/PIA12235~medium.jpg"
      }
    ]
  }
  ```

### 3. Moon APOD (Astronomy Picture of the Day)

- **URL:** `/moon/apod`
- **Method:** `GET`
- **Description:** Fetches recent APOD entries and filters for moon-related content.
- **Query Parameters:**
  - `api_key` (String, default: `"DEMO_KEY"`): NASA API key. Use `DEMO_KEY` for development (rate-limited).
- **Response:**
  ```json
  {
    "source": "NASA APOD",
    "count": 1,
    "results": [
      {
        "title": "The Reappearance of Mars",
        "explanation": "Mars reappears just beyond the Moon's dark limb...",
        "date": "2020-09-11",
        "image_url": "https://apod.nasa.gov/apod/image/2009/MarsReappearanceDuarte.jpg"
      }
    ]
  }
  ```

### 4. Moon Overview

- **URL:** `/moon`
- **Method:** `GET`
- **Description:** Combines data from both NASA Image Library (total hit count + sample images) and APOD into a single response.
- **Response:**
  ```json
  {
    "total_images": 19605,
    "sample_images": [ ... ],
    "apod_entries": [ ... ]
  }
  ```

## Rate Limiting

Using the `DEMO_KEY` API key has a rate limit of 30 requests per hour. For heavier usage, get a free API key at https://api.nasa.gov.

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`. Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
