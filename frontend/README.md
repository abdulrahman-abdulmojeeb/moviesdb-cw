# Movies DB - Frontend

React frontend for the COMP0022 Movies Database project.

## Tech Stack

- React 19
- Vite 6
- Tailwind CSS v4
- React Router v7
- Axios (API client)
- Recharts (visualisations)

## Pages

- **Dashboard** (`/`) - Browse, search, filter movies
- **Movie Detail** (`/movies/:id`) - Full movie info with cast, crew, ratings
- **Genre Reports** (`/reports/genres`) - Genre popularity and polarisation charts
- **Rating Patterns** (`/reports/ratings`) - Rating bias and cross-genre analysis
- **Predictions** (`/predictions`) - Predictive ratings
- **Personality** (`/reports/personality`) - Big Five personality insights
- **Collections** (`/collections`) - User's movie collections
- **Login/Register** (`/login`, `/register`) - Authentication

## Development

```bash
# Run via Docker (recommended)
cd ../infra && docker compose up -d

# Or run locally
npm install
npm run dev
```

Visit http://localhost:5173 when running.
