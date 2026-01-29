export default function MovieFilters({
  genres,
  selectedGenre,
  onGenreChange,
  yearMin,
  yearMax,
  onYearMinChange,
  onYearMaxChange,
  sortBy,
  onSortChange,
  order,
  onOrderChange,
}) {
  return (
    <div className="flex flex-wrap gap-3 items-center">
      <select
        value={selectedGenre || ""}
        onChange={(e) => onGenreChange(e.target.value || null)}
        className="px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:border-blue-500"
      >
        <option value="">All Genres</option>
        {genres.map((g) => (
          <option key={g.genre_id} value={g.genre_id}>
            {g.name}
          </option>
        ))}
      </select>

      <input
        type="number"
        value={yearMin || ""}
        onChange={(e) => onYearMinChange(e.target.value || null)}
        placeholder="Year from"
        min={1900}
        max={2030}
        className="w-28 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
      />
      <input
        type="number"
        value={yearMax || ""}
        onChange={(e) => onYearMaxChange(e.target.value || null)}
        placeholder="Year to"
        min={1900}
        max={2030}
        className="w-28 px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
      />

      <select
        value={sortBy}
        onChange={(e) => onSortChange(e.target.value)}
        className="px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:border-blue-500"
      >
        <option value="title">Sort by Title</option>
        <option value="year">Sort by Year</option>
        <option value="rating">Sort by Rating</option>
      </select>

      <button
        onClick={() => onOrderChange(order === "asc" ? "desc" : "asc")}
        className="px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-white hover:bg-gray-800 transition"
      >
        {order === "asc" ? "Asc" : "Desc"}
      </button>
    </div>
  );
}
