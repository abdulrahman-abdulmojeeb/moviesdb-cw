import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

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
            <Link to="/reports/genres" className="text-gray-300 hover:text-white transition">
              Genre Reports
            </Link>
            <Link to="/reports/ratings" className="text-gray-300 hover:text-white transition">
              Rating Patterns
            </Link>
            <Link to="/predictions" className="text-gray-300 hover:text-white transition">
              Predictions
            </Link>
            <Link to="/reports/personality" className="text-gray-300 hover:text-white transition">
              Personality
            </Link>
          </div>
        </div>
        <div className="flex items-center gap-3 text-sm">
          {user ? (
            <>
              <span className="text-gray-400">{user.display_name || user.username}</span>
              <button
                onClick={handleLogout}
                className="px-3 py-1.5 rounded bg-gray-800 text-gray-300 hover:bg-gray-700 transition"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-3 py-1.5 rounded text-gray-300 hover:text-white transition"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-500 transition"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
