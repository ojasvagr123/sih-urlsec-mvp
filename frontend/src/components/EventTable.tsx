import type { EventRow } from "../lib/api"

export default function EventTable({ rows }: { rows: EventRow[] }) {
  return (
    <div className="overflow-x-auto border border-slate-800 rounded-lg">
      <table className="w-full text-sm">
        <thead className="bg-slate-800/50 border-b border-slate-700">
          <tr>
            <th className="text-left p-2">Time</th>
            <th className="text-left p-2">IP</th>
            <th className="text-left p-2">Method</th>
            <th className="text-left p-2">URL</th>
            <th className="text-left p-2">Attack</th>
            <th className="text-left p-2">Conf</th>
            <th className="text-left p-2">Success</th>
            <th className="text-left p-2">HP Session</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="odd:bg-slate-900 even:bg-slate-950">
              <td className="p-2">{r.timestamp}</td>
              <td className="p-2">{r.src_ip}</td>
              <td className="p-2">{r.method}</td>
              <td className="p-2 max-w-[420px] truncate">{r.url}</td>
              <td className="p-2">{r.attack_type}</td>
              <td className="p-2">{r.attack_confidence}</td>
              <td className="p-2">{String(r.is_success)}</td>
              <td className="p-2">{r.honeypot_session}</td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr>
              <td colSpan={8} className="text-center text-slate-400 p-6">No events yet.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
