import { useEffect, useMemo, useState } from "react"
import Filters from "../components/Filters"
import EventTable from "../components/EventTable"
import StatCard from "../components/StatCard"
import { fetchEvents, type EventRow } from "../lib/api"

export default function Dashboard() {
  const [rows, setRows] = useState<EventRow[]>([])
  const [q, setQ] = useState<{ attack_type?: string; ip?: string; success?: string }>({})

  useEffect(() => {
    fetchEvents(q).then(setRows).catch(console.error)
  }, [q])

  const stats = useMemo(() => {
    const total = rows.length
    const honeypot = rows.filter(r => r.honeypot_correlated).length
    const success = rows.filter(r => r.is_success).length
    return { total, honeypot, success }
  }, [rows])

  return (
    <div className="space-y-4">
      <Filters onApply={setQ} />

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <StatCard label="Total Events" value={stats.total} />
        <StatCard label="Honeypot Hits" value={stats.honeypot} />
        <StatCard label="Successful Attacks" value={stats.success} />
      </div>

      <EventTable rows={rows} />
    </div>
  )
}
