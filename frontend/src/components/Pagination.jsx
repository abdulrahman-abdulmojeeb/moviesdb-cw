export default function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const pages = [];
  const start = Math.max(1, page - 2);
  const end = Math.min(totalPages, page + 2);

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  return (
    <nav className="flex items-center justify-center gap-2 mt-8" aria-label="Pagination">
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        aria-label="Previous page"
        className="px-3 py-1.5 rounded bg-gray-900 border border-gray-700 text-sm text-gray-300 hover:bg-gray-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        Prev
      </button>
      {start > 1 && (
        <>
          <button
            onClick={() => onPageChange(1)}
            aria-label="Page 1"
            className="px-3 py-1.5 rounded bg-gray-900 border border-gray-700 text-sm text-gray-300 hover:bg-gray-800 transition"
          >
            1
          </button>
          {start > 2 && <span className="text-gray-600">...</span>}
        </>
      )}
      {pages.map((p) => (
        <button
          key={p}
          onClick={() => onPageChange(p)}
          aria-label={`Page ${p}`}
          aria-current={p === page ? "page" : undefined}
          className={`px-3 py-1.5 rounded border text-sm transition ${
            p === page
              ? "bg-blue-600 border-blue-600 text-white"
              : "bg-gray-900 border-gray-700 text-gray-300 hover:bg-gray-800"
          }`}
        >
          {p}
        </button>
      ))}
      {end < totalPages && (
        <>
          {end < totalPages - 1 && <span className="text-gray-600">...</span>}
          <button
            onClick={() => onPageChange(totalPages)}
            aria-label={`Page ${totalPages}`}
            className="px-3 py-1.5 rounded bg-gray-900 border border-gray-700 text-sm text-gray-300 hover:bg-gray-800 transition"
          >
            {totalPages}
          </button>
        </>
      )}
      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
        aria-label="Next page"
        className="px-3 py-1.5 rounded bg-gray-900 border border-gray-700 text-sm text-gray-300 hover:bg-gray-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        Next
      </button>
    </nav>
  );
}
