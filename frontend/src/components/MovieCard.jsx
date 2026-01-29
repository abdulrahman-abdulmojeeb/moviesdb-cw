import { Link } from "react-router-dom";
import { TMDB_POSTER_W300 } from "../constants";

export default function MovieCard({ movie }) {
  const poster = movie.poster_path
    ? `${TMDB_POSTER_W300}${movie.poster_path}`
    : null;

  return (
    <Link
      to={`/movies/${movie.movie_id}`}
      className="group bg-gray-900 rounded-lg overflow-hidden border border-gray-800 hover:border-gray-600 transition"
    >
      <div className="aspect-[2/3] bg-gray-800 relative">
        {poster ? (
          <img
            src={poster}
            alt={movie.title}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-600 text-sm px-4 text-center">
            {movie.title}
          </div>
        )}
        {movie.avg_rating && (
          <span className="absolute top-2 right-2 bg-black/80 text-yellow-400 text-xs font-semibold px-2 py-1 rounded">
            {Number(movie.avg_rating).toFixed(1)}
          </span>
        )}
      </div>
      <div className="p-3">
        <h3 className="font-medium text-sm text-white truncate group-hover:text-blue-400 transition">
          {movie.title}
        </h3>
        <p className="text-xs text-gray-500 mt-1">
          {movie.release_year || "Unknown year"}
          {movie.genres && ` · ${movie.genres}`}
        </p>
      </div>
    </Link>
  );
}
