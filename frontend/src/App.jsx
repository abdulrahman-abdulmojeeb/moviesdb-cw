import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ErrorBoundary from "./components/ErrorBoundary";
import DashboardPage from "./pages/DashboardPage";
import MovieDetailPage from "./pages/MovieDetailPage";
import GenreReportsPage from "./pages/GenreReportsPage";
import RatingPatternsPage from "./pages/RatingPatternsPage";
import PredictionsPage from "./pages/PredictionsPage";
import PersonalityPage from "./pages/PersonalityPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
        <ErrorBoundary>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/movies/:id" element={<MovieDetailPage />} />
            <Route path="/reports/genres" element={<GenreReportsPage />} />
            <Route path="/reports/ratings" element={<RatingPatternsPage />} />
            <Route path="/predictions" element={<PredictionsPage />} />
            <Route path="/reports/personality" element={<PersonalityPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </ErrorBoundary>
      </main>
    </div>
  );
}
