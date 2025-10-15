import { useEffect, useMemo, useState } from "react"
import Filters from "../components/Filters"
import EventTable from "../components/EventTable"
import StatCard from "../components/StatCard"
import { fetchEvents, type EventRow } from "../lib/api"

export default function Dashboard() {
  const [rows, setRows] = useState<EventRow[]>([])
  const [q, setQ] = useState<{ attack_type?: string; ip?: string; success?: string }>({})
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    fetchEvents(q).then(setRows).catch(console.error)
  }, [q])

  const stats = useMemo(() => {
    const total = rows.length
    const honeypot = rows.filter(r => r.honeypot_correlated).length
    const success = rows.filter(r => r.is_success).length
    return { total, honeypot, success }
  }, [rows])

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    if (!file.name.endsWith(".pcap")) {
      alert("Please upload a valid .pcap file.")
      return
    }

    setUploading(true)
    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/upload/pcap`, {
        method: "POST",
        body: formData,
      })
      const data = await res.json()
      alert(`Uploaded successfully! Parsed ${data.parsed_events || 0} events.`)
      fetchEvents(q).then(setRows) // refresh events
    } catch (err) {
      console.error(err)
      alert("Upload failed.")
    } finally {
      setUploading(false)
      e.target.value = "" // reset file input
    }
  }

  return (
    <div className="space-y-4">
      {/* Upload Section */}
      <div className="flex items-center space-x-3">
        <label className="block">
          <input
            type="file"
            accept=".pcap"
            disabled={uploading}
            onChange={handleUpload}
            className="text-sm text-slate-300 file:mr-3 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer"
          />
        </label>
        {uploading && <span className="text-blue-400 text-sm">Uploading...</span>}
      </div>

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
