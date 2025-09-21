import { Routes, Route, NavLink, useLocation, Navigate } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Cowrie from "./pages/Cowrie"
import Login from "./pages/Login"
import { useState } from "react"

export default function App() {
  const navLinkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium ${isActive ? "bg-blue-600 text-white" : "text-blue-300 hover:bg-blue-800/40"}`
  
  // fake login state
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const location = useLocation()

  // If not logged in → redirect to login (except when already on /login)
  if (!isLoggedIn && location.pathname !== "/login") {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="min-h-screen flex flex-col">
      

        {/* 🔹 Header */}
<header className="border-b border-slate-800 bg-slate-950">
  <div className="mx-auto max-w-7xl px-4 py-4 flex items-center justify-between">
    {/* Left: Niyantrak logo + title */}
    <div className="flex items-center space-x-3">
      <img src="/logo1.png" alt="Niyantrak Logo" className="h-12 w-auto" />
      <h1 className="text-2xl font-bold text-blue-400">नियंत्रक</h1>
    </div>

    {/* Center: Subtitle */}
    <div className="hidden md:block">
      <p className="text-slate-300 text-sm font-medium">
        Cybersecurity Attack Detection & Honeypot Correlation
      </p>
    </div>

    {/* Right: NTRO logo */}
    <div className="flex items-center space-x-3">
      <span className="text-slate-300 text-sm font-medium">
        राष्ट्रीय तकनीकी अनुसंधान संगठन
      </span>
      <img src="/logo2.png" alt="NTRO Logo" className="h-12 w-auto" />
    </div>
  </div>

  {/* 🔹 Show nav only if logged in */}
  {isLoggedIn && (
    <nav className="bg-slate-900 border-t border-slate-800 px-4 py-2 flex space-x-2 justify-center">
      <NavLink to="/" className={navLinkClass} end>Dashboard</NavLink>
      <NavLink to="/cowrie" className={navLinkClass}>Cowrie Logs</NavLink>
    </nav>
  )}
</header>

      {/* Main content */}
      <main className="px-6 py-6 flex-grow">
      <Routes>
        <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/cowrie" element={<Cowrie />} />
      </Routes>
    </main>


      {/* Footer */}
      <footer className="border-t border-slate-800 text-slate-400 text-xs py-4 text-center">
        नियंत्रणक (Niyantrak) • API: <code>{import.meta.env.VITE_API_URL || "http://localhost:8000"}</code>
      </footer>
    </div>
  )
}
