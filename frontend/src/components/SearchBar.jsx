import { useState, useEffect } from "react";

export default function SearchBar({ value, onChange, placeholder = "Search movies..." }) {
  const [input, setInput] = useState(value || "");

  useEffect(() => {
    setInput(value || "");
  }, [value]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onChange(input);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        className="flex-1 px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition"
      >
        Search
      </button>
    </form>
  );
}
