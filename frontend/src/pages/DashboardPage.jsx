import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import client from "../api/client";
import SearchBar from "../components/SearchBar";
import MovieFilters from "../components/MovieFilters";
import MovieGrid from "../components/MovieGrid";
import Pagination from "../components/Pagination";
import { DEFAULT_PER_PAGE } from "../constants";

export default function DashboardPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const query = searchParams.get("q") || "";
  const selectedGenre = searchParams.get("genre_id") ? Number(searchParams.get("genre_id")) : null;
  const yearMin = searchParams.get("year_min") ? Number(searchParams.get("year_min")) : null;
  const yearMax = searchParams.get("year_max") ? Number(searchParams.get("year_max")) : null;
  const sortBy = searchParams.get("sort_by") || "title";
  const order = searchParams.get("order") || "asc";
  const page = searchParams.get("page") ? Number(searchParams.get("page")) : 1;
  const [totalPages, setTotalPages] = useState(1);

  const updateParams = (updates) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      for (const [key, value] of Object.entries(updates)) {
        if (value === null || value === undefined || value === "") {
          next.delete(key);
        } else {
          next.set(key, String(value));
        }
      }
      return next;
    });
  };

  useEffect(() => {
    const controller = new AbortController();
    client
      .get("/genres", { signal: controller.signal })
      .then((res) => setGenres(res.data))
      .catch((err) => {
        if (!controller.signal.aborted) setError("Failed to load genres");
      });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    client
      .get("/movies", {
        params: {
          q: query || undefined,
          genre_id: selectedGenre || undefined,
          year_min: yearMin || undefined,
          year_max: yearMax || undefined,
          sort_by: sortBy,
          order,
          page,
          per_page: DEFAULT_PER_PAGE,
        },
        signal: controller.signal,
      })
      .then((res) => {
        setMovies(res.data.movies);
        setTotalPages(res.data.total_pages);
      })
      .catch((err) => {
        if (!controller.signal.aborted) {
          setMovies([]);
          setError("Failed to load movies. Please try again.");
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [query, selectedGenre, yearMin, yearMax, sortBy, order, page]);

  const handleSearch = (value) => updateParams({ q: value, page: null });
  const handleGenreChange = (value) => updateParams({ genre_id: value, page: null });
  const handleYearMinChange = (value) => updateParams({ year_min: value, page: null });
  const handleYearMaxChange = (value) => updateParams({ year_max: value, page: null });
  const handleSortChange = (value) => updateParams({ sort_by: value, page: null });
  const handleOrderChange = (value) => updateParams({ order: value, page: null });
  const handlePageChange = (newPage) => {
    updateParams({ page: newPage > 1 ? newPage : null });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="space-y-6">
      <SearchBar value={query} onChange={handleSearch} />
      <MovieFilters
        genres={genres}
        selectedGenre={selectedGenre}
        onGenreChange={handleGenreChange}
        yearMin={yearMin}
        yearMax={yearMax}
        onYearMinChange={handleYearMinChange}
        onYearMaxChange={handleYearMaxChange}
        sortBy={sortBy}
        onSortChange={handleSortChange}
        order={order}
        onOrderChange={handleOrderChange}
      />
      {error && (
        <div className="text-center py-4 text-red-400 bg-red-900/20 border border-red-800 rounded-lg">
          {error}
        </div>
      )}
      <MovieGrid movies={movies} loading={loading} />
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange} />
    </div>
  );
}
