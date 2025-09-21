const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

export type EventRow = {
  id: number
  timestamp: string
  src_ip: string
  dst_ip?: string
  method?: string
  url?: string
  params?: Record<string, unknown> | null
  headers?: Record<string, unknown> | null
  body?: string | null
  body_snippet?: string | null
  attack_type?: string | null
  attack_confidence?: number | null
  is_success?: boolean | null
  honeypot_correlated?: boolean | null
  honeypot_session?: string | null
}

export type CowrieRow = {
  id: number
  timestamp: string
  src_ip: string
  event: string
  username?: string | null
  password?: string | null
  session?: string | null
}

export async function fetchEvents(params?: {
  attack_type?: string
  ip?: string
  success?: string
}): Promise<EventRow[]> {
  const q = new URLSearchParams()
  if (params?.attack_type) q.set("attack_type", params.attack_type)
  if (params?.ip) q.set("ip", params.ip)
  if (params?.success) q.set("success", params.success)
  const res = await fetch(`${API}/events?${q.toString()}`)
  if (!res.ok) throw new Error("Failed to fetch events")
  return res.json()
}

export async function fetchExportJSON(): Promise<EventRow[]> {
  const res = await fetch(`${API}/export.json`)
  if (!res.ok) throw new Error("Failed to export json")
  return res.json()
}

export async function fetchCowrie(params?: {
  ip?: string
  event?: string
}): Promise<CowrieRow[]> {
  const q = new URLSearchParams()
  if (params?.ip) q.set("ip", params.ip)
  if (params?.event) q.set("event", params.event)
  const res = await fetch(`${API}/cowrie/export.json?${q.toString()}`)
  if (!res.ok) throw new Error("Failed to fetch cowrie")
  return res.json()
}
