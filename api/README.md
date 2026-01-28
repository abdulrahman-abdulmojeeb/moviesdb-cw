# Movies DB - API

FastAPI backend for the COMP0022 Movies Database project.

## Endpoints

### Movies (R1)
- `GET /api/movies` - Search, filter, paginate movies
- `GET /api/movies/{id}` - Full movie detail with cast, crew, genres
- `GET /api/genres` - List all genres

### Genre Reports (R2)
- `GET /api/reports/genre-popularity` - Genre popularity metrics
- `GET /api/reports/genre-polarisation` - Genre rating variance

### Rating Patterns (R3)
- `GET /api/reports/rating-bias` - User rating bias analysis
- `GET /api/reports/cross-genre-preferences` - Cross-genre correlation

### Predictions (R4)
- `POST /api/predictions/predict` - Predict rating for user+movie
- `GET /api/predictions/similar-films/{id}` - Find similar films

### Personality (R5)
- `GET /api/reports/personality-genre-correlation` - Big Five trait correlations
- `GET /api/reports/personality-clusters` - Personality-based clusters

### Collections (R6)
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login, returns JWT
- `GET /api/auth/me` - Current user info
- `GET /api/collections` - List user's collections
- `POST /api/collections` - Create collection
- `GET /api/collections/{id}` - Get collection with items
- `PUT /api/collections/{id}` - Update collection
- `DELETE /api/collections/{id}` - Delete collection
- `POST /api/collections/{id}/items` - Add movie to collection
- `DELETE /api/collections/{id}/items/{movie_id}` - Remove movie

## Development

```bash
# Run via Docker (recommended)
cd ../infra && docker compose up -d

# Or run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

When running, visit http://localhost:8000/docs for Swagger UI.
