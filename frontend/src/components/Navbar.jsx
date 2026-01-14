import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-xl font-bold text-white">
            Movies DB
          </Link>
          <div className="hidden md:flex items-center gap-4 text-sm">
            <Link to="/" className="text-gray-300 hover:text-white transition">
              Browse
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
