import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import client from "../api/client";
import { TMDB_POSTER_W500, TMDB_BACKDROP_ORIGINAL } from "../constants";

function formatCurrency(value) {
  if (!value) return null;
  return `$${Number(value).toLocaleString()}`;
}

export default function MovieDetailPage() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    client
      .get(`/movies/${id}`, { signal: controller.signal })
      .then((res) => setMovie(res.data))
      .catch((err) => {
        if (!controller.signal.aborted) setMovie(null);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [id]);

  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-72 bg-gray-800 rounded-xl" />
        <div className="flex gap-8">
          <div className="w-64 shrink-0 aspect-[2/3] bg-gray-800 rounded-lg" />
          <div className="flex-1 space-y-4">
            <div className="h-8 bg-gray-800 rounded w-1/2" />
            <div className="h-4 bg-gray-800 rounded w-1/4" />
            <div className="h-20 bg-gray-800 rounded" />
          </div>
        </div>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="text-center py-20 text-gray-500">Movie not found.</div>
    );
  }

  const director = movie.crew?.find((c) => c.job === "Director");
  const backdrop = movie.backdrop_path
    ? `${TMDB_BACKDROP_ORIGINAL}${movie.backdrop_path}`
    : null;
  const poster = movie.poster_path
    ? `${TMDB_POSTER_W500}${movie.poster_path}`
    : null;

  return (
    <div className="space-y-6">
      {/* Backdrop hero banner */}
      {backdrop && (
        <div className="relative h-72 md:h-96 rounded-xl overflow-hidden -mx-4 -mt-6">
          <img
            src={backdrop}
            alt=""
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-gray-950 via-gray-950/60 to-transparent" />
        </div>
      )}

      {/* Main content */}
      <div className="flex flex-col md:flex-row gap-8">
        {/* Poster */}
        <div className="w-56 md:w-64 shrink-0 mx-auto md:mx-0">
          {poster ? (
            <img
              src={poster}
              alt={movie.title}
              className="w-full rounded-lg shadow-lg"
            />
          ) : (
            <div className="aspect-[2/3] bg-gray-800 rounded-lg flex items-center justify-center text-gray-600">
              No Poster
            </div>
          )}
        </div>

        {/* Details */}
        <div className="flex-1 space-y-5">
          <div>
            <h1 className="text-3xl font-bold text-white">{movie.title}</h1>
            <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-gray-400">
              {movie.release_year && <span>{movie.release_year}</span>}
              {movie.runtime_minutes && (
                <span>{movie.runtime_minutes} min</span>
              )}
              {director && <span>Directed by {director.name}</span>}
            </div>
          </div>

          {/* Ratings */}
          <div className="flex flex-wrap gap-4 text-sm">
            {movie.avg_rating && (
              <div className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded-lg">
                <span className="text-yellow-400 font-semibold">
                  {Number(movie.avg_rating).toFixed(1)}
                </span>
                <span className="text-gray-500 ml-1">
                  ({movie.rating_count} ratings)
                </span>
              </div>
            )}
            {movie.imdb_rating && (
              <div className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded-lg">
                <span className="text-gray-300">IMDb</span>{" "}
                <span className="text-white font-semibold">
                  {movie.imdb_rating}
                </span>
              </div>
            )}
            {movie.rotten_tomatoes_score && (
              <div className="px-3 py-1.5 bg-gray-900 border border-gray-700 rounded-lg">
                <span className="text-gray-300">RT</span>{" "}
                <span className="text-white font-semibold">
                  {movie.rotten_tomatoes_score}%
                </span>
              </div>
            )}
          </div>

          {/* Genres */}
          {movie.genres?.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {movie.genres.map((g) => (
                <span
                  key={g.genre_id}
                  className="px-3 py-1 bg-gray-800 border border-gray-700 rounded-full text-xs text-gray-300"
                >
                  {g.name}
                </span>
              ))}
            </div>
          )}

          {/* Overview */}
          {movie.overview && (
            <p className="text-gray-300 leading-relaxed">{movie.overview}</p>
          )}

          {/* Financial info */}
          {(movie.budget || movie.revenue || movie.box_office) && (
            <div className="flex flex-wrap gap-6 text-sm">
              {movie.budget && (
                <div>
                  <span className="text-gray-500">Budget</span>
                  <p className="text-white font-medium">
                    {formatCurrency(movie.budget)}
                  </p>
                </div>
              )}
              {movie.revenue && (
                <div>
                  <span className="text-gray-500">Revenue</span>
                  <p className="text-white font-medium">
                    {formatCurrency(movie.revenue)}
                  </p>
                </div>
              )}
              {movie.box_office && (
                <div>
                  <span className="text-gray-500">Box Office</span>
                  <p className="text-white font-medium">
                    {formatCurrency(movie.box_office)}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Tags */}
          {movie.tags?.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 mb-2">
                Tags
              </h2>
              <div className="flex flex-wrap gap-2">
                {movie.tags.map((t) => (
                  <span
                    key={t.tag}
                    className="px-2.5 py-1 bg-blue-900/30 border border-blue-800/50 rounded-full text-xs text-blue-300"
                  >
                    {t.tag}
                    {t.count > 1 && (
                      <span className="ml-1 text-blue-500">({t.count})</span>
                    )}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Cast */}
          {movie.cast?.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 mb-3">
                Cast
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {movie.cast.map((member) => (
                  <div
                    key={`${member.person_id}-${member.character}`}
                    className="flex items-center gap-3"
                  >
                    {member.profile_path ? (
                      <img
                        src={`${TMDB_POSTER_W500}${member.profile_path}`}
                        alt={member.name}
                        className="w-10 h-10 rounded-full object-cover"
                      />
                    ) : (
                      <div className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center text-gray-600 text-xs">
                        ?
                      </div>
                    )}
                    <div className="min-w-0">
                      <p className="text-sm text-white truncate">
                        {member.name}
                      </p>
                      {member.character && (
                        <p className="text-xs text-gray-500 truncate">
                          {member.character}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Crew */}
          {movie.crew?.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-gray-400 mb-2">
                Crew
              </h2>
              <div className="flex flex-wrap gap-4 text-sm">
                {movie.crew.map((member) => (
                  <div key={`${member.person_id}-${member.job}`}>
                    <span className="text-white">{member.name}</span>
                    <span className="text-gray-500 ml-1">({member.job})</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
