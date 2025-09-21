import { useState } from "react"
import { useNavigate } from "react-router-dom"

export default function Login({ onLogin }: { onLogin: () => void }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // fake validation
    if (username && password) {
      onLogin()
      navigate("/") // ✅ redirect to Dashboard
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900">
      <div className="w-full max-w-sm bg-slate-800 p-8 rounded-xl shadow-lg">
        
        {/* Logo on top */}
        <div className="flex justify-center mb-6">
          <img src="/logo1.png" alt="Niyantrak Logo" className="h-16 w-auto" />
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-slate-300 mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="+910000000000"
              className="w-full px-4 py-2 rounded-lg bg-slate-700 border border-slate-600 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-slate-700 border border-slate-600 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg font-medium transition"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  )
}
