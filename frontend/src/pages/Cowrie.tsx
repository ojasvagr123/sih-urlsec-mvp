import { useEffect, useState } from "react"
import { fetchCowrie, type CowrieRow } from "../lib/api"

export default function Cowrie() {
  const [rows, setRows] = useState<CowrieRow[]>([])
  const [ip, setIp] = useState("")
  const [event, setEvent] = useState("")

  useEffect(() => {
    fetchCowrie({ ip: ip || undefined, event: event || undefined }).then(setRows).catch(console.error)
  }, [ip, event])

  return (
    <div className="space-y-4">
        {/* 🔹 Button at the top */}
      <div className="mb-4">
        <a
          href="http://13.48.133.89/"
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded shadow"
        >
          Open Honeypot Dashboard
        </a>
      </div>

      <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-4">
        <div className="flex flex-wrap items-end gap-3">
          <div>
            <label className="block text-sm text-slate-300">IP</label>
            <input
              className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm"
              placeholder="1.2.3.4"
              value={ip}
              onChange={(e) => setIp(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300">Event contains</label>
            <input
              className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm"
              placeholder="success / fail"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="overflow-x-auto border border-slate-800 rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-slate-800/50 border-b border-slate-700">
            <tr>
              <th className="text-left p-2">Time</th>
              <th className="text-left p-2">IP</th>
              <th className="text-left p-2">Event</th>
              <th className="text-left p-2">User</th>
              <th className="text-left p-2">Pass</th>
              <th className="text-left p-2">Session</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id} className="odd:bg-slate-900 even:bg-slate-950">
                <td className="p-2">{r.timestamp}</td>
                <td className="p-2">{r.src_ip}</td>
                <td className="p-2">{r.event}</td>
                <td className="p-2">{r.username}</td>
                <td className="p-2">{r.password}</td>
                <td className="p-2">{r.session}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={6} className="text-center text-slate-400 p-6">No Cowrie logs yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
