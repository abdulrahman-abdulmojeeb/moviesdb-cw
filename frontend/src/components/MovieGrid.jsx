import MovieCard from "./MovieCard";

export default function MovieGrid({ movies, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {Array.from({ length: 20 }).map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="aspect-[2/3] bg-gray-800 rounded-lg" />
            <div className="mt-2 h-4 bg-gray-800 rounded w-3/4" />
            <div className="mt-1 h-3 bg-gray-800 rounded w-1/2" />
          </div>
        ))}
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <div className="text-center py-20 text-gray-500">
        No movies found.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {movies.map((movie) => (
        <MovieCard key={movie.movie_id} movie={movie} />
      ))}
    </div>
  );
}
