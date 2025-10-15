import { Routes, Route, NavLink } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Cowrie from "./pages/Cowrie"
import AnalyticsDashboard from "./pages/AnalyticsDashboard"

export default function App() {
  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
      isActive
        ? "bg-blue-600 text-white"
        : "text-blue-300 hover:bg-blue-800/40"
    }`


  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950">
        <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
          {/* Left */}
          <div className="flex items-center space-x-3">
            <img src="/logo1.png" alt="Niyantrak Logo" className="h-12 w-auto" />
            <h1 className="text-2xl font-bold text-blue-400">नियंत्रक</h1>
          </div>

          {/* Center */}
          <div className="hidden md:block">
            <p className="text-slate-300 text-sm font-medium">
              Cybersecurity Attack Detection & Honeypot Correlation
            </p>
          </div>

          {/* Right */}
          <div className="flex items-center space-x-3">
            <span className="text-slate-300 text-sm font-medium text-right">
              राष्ट्रीय तकनीकी अनुसंधान संगठन
            </span>
            <img src="/logo2.png" alt="NTRO Logo" className="h-12 w-auto" />
          </div>
        </div>

        {/* Navigation */}
        <nav className="bg-slate-900 border-t border-slate-800 px-4 py-2 flex flex-wrap justify-center space-x-2">
          <NavLink to="/" className={navLinkClass} end>
            Dashboard
          </NavLink>
          <NavLink to="/cowrie" className={navLinkClass}>
            Cowrie Logs
          </NavLink>
          <NavLink to="/analytics" className={navLinkClass}>
            Analytics
          </NavLink>
        </nav>
      </header>

      {/* Main */}
      <main className="px-6 py-6 flex-grow">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/cowrie" element={<Cowrie />} />
          <Route path="/analytics" element={<AnalyticsDashboard />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 text-slate-400 text-xs py-4 text-center">
        नियंत्रणक (Niyantrak) • API:&nbsp;
        <code>{import.meta.env.VITE_API_URL || "http://localhost:8000"}</code>
      </footer>
    </div>
  )
}
