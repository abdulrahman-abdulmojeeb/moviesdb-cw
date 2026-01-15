#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────
# Movies DB – One-command bootstrap
# Usage: ./setup.sh [--skip-enrich]
# ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
DATA_DIR="$ROOT_DIR/data"
SKIP_ENRICH=false

for arg in "$@"; do
  case $arg in
    --skip-enrich) SKIP_ENRICH=true ;;
  esac
done

# Colours
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── 1. Check prerequisites ──────────────────
info "Checking prerequisites..."
command -v docker  >/dev/null 2>&1 || error "docker is not installed"
command -v docker  >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 || error "docker compose v2 is required"
command -v curl    >/dev/null 2>&1 || error "curl is not installed"
command -v unzip   >/dev/null 2>&1 || error "unzip is not installed"

# ── 2. Download datasets ────────────────────
mkdir -p "$DATA_DIR"

MOVIELENS_URL="https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
MOVIELENS_ZIP="$DATA_DIR/ml-latest-small.zip"
PERSONALITY_URL="https://raw.githubusercontent.com/kganeshchandan/PERSONALITY_ISF_2018/master"

if [ ! -f "$DATA_DIR/movies.csv" ]; then
  info "Downloading MovieLens small dataset..."
  curl -L -o "$MOVIELENS_ZIP" "$MOVIELENS_URL"
  unzip -o "$MOVIELENS_ZIP" -d "$DATA_DIR"
  # Flatten: move files from ml-latest-small/ to data/
  mv "$DATA_DIR/ml-latest-small/"* "$DATA_DIR/" 2>/dev/null || true
  rm -rf "$DATA_DIR/ml-latest-small" "$MOVIELENS_ZIP"
  info "MovieLens data ready."
else
  info "MovieLens data already present, skipping download."
fi

if [ ! -f "$DATA_DIR/personality-data.csv" ]; then
  info "Downloading Personality ISF 2018 dataset..."
  curl -L -o "$DATA_DIR/personality-data.csv" "$PERSONALITY_URL/personality-data.csv"
  curl -L -o "$DATA_DIR/personality-ratings.csv" "$PERSONALITY_URL/ratings.csv"
  info "Personality data ready."
else
  info "Personality data already present, skipping download."
fi

# ── 3. Copy .env if missing ─────────────────
if [ ! -f "$ROOT_DIR/.env" ]; then
  info "Creating .env from .env.example..."
  cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
  warn "Review $ROOT_DIR/.env and add API keys if needed."
fi

# ── 4. Build & start containers ─────────────
info "Building and starting containers..."
cd "$ROOT_DIR"
docker compose up -d --build

# Wait for API to be ready
info "Waiting for API to be ready..."
for i in $(seq 1 30); do
  if curl -sf "http://localhost:${API_PORT:-8000}/health" >/dev/null 2>&1; then
    info "API is ready."
    break
  fi
  if [ "$i" -eq 30 ]; then
    error "API did not become ready in time. Check logs: docker compose logs api"
  fi
  sleep 2
done

# ── 5. Run migrations ───────────────────────
info "Running database migrations..."
docker compose exec api python db/migrate.py

# ── 6. Seed data ────────────────────────────
info "Loading MovieLens data..."
docker compose exec api python db/seed/load_movielens.py

info "Loading Personality data..."
docker compose exec api python db/seed/load_personality.py

# ── 7. Optional enrichment ──────────────────
if [ "$SKIP_ENRICH" = false ]; then
  source "$ROOT_DIR/.env"
  if [ -n "${TMDB_API_KEY:-}" ]; then
    info "Enriching with TMDB data..."
    docker compose exec api python db/seed/load_tmdb.py
  else
    warn "TMDB_API_KEY not set. Skipping TMDB enrichment."
  fi
  if [ -n "${OMDB_API_KEY:-}" ]; then
    info "Enriching with OMDB data..."
    docker compose exec api python db/seed/load_omdb.py
  else
    warn "OMDB_API_KEY not set. Skipping OMDB enrichment."
  fi
else
  warn "Skipping enrichment (--skip-enrich)."
fi

# ── 8. Done ─────────────────────────────────
echo ""
info "========================================="
info "  Movies DB is ready!"
info "========================================="
info "  API:      http://localhost:8000"
info "  API Docs: http://localhost:8000/docs"
info "  Frontend: http://localhost:5173"
info "========================================="
