import React, { useEffect, useState } from "react"
import axios from "axios"
import Chart from "react-apexcharts"

interface AttackType {
  type: string
  count: number
}

interface AttackTrend {
  date: string
  count: number
}

interface AttackIP {
  ip: string
  count: number
}

interface AnalyticsData {
  total_attacks: number
  successful_attacks: number
  top_attacks: AttackType[]
  top_ips: AttackIP[]
  trend: AttackTrend[]
}

const AnalyticsDashboard: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null)

  useEffect(() => {
    axios
      .get<AnalyticsData>(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/analytics`)
      .then((res) => setData(res.data))
      .catch((err) => console.error("Failed to fetch analytics", err))
  }, [])

  if (!data) {
    return <p className="text-slate-300">Loading analytics...</p>
  }

  const pieOptions = {
    labels: data.top_attacks.map((a) => a.type),
    theme: { mode: "dark" as const },
    chart: { background: "transparent" },
  }

  const pieSeries = data.top_attacks.map((a) => a.count)

  const trendOptions = {
    chart: { id: "attack-trend", toolbar: { show: false } },
    xaxis: { categories: data.trend.map((t) => t.date) },
    theme: { mode: "dark" as const },
    stroke: { curve: "smooth" as const },
  }

  const trendSeries = [
    {
      name: "Attacks",
      data: data.trend.map((t) => t.count),
    },
  ]

  return (
    <div className="text-white space-y-6">
      <h2 className="text-2xl font-semibold mb-2">Attack Analytics Dashboard</h2>

      {/* Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-slate-800 p-4 rounded-lg text-center">
          <p className="text-slate-400 text-sm">Total Attacks</p>
          <h3 className="text-2xl font-bold">{data.total_attacks}</h3>
        </div>
        <div className="bg-slate-800 p-4 rounded-lg text-center">
          <p className="text-slate-400 text-sm">Successful Attacks</p>
          <h3 className="text-2xl font-bold text-green-400">{data.successful_attacks}</h3>
        </div>
      </div>

      {/* Charts */}
      <div className="flex flex-wrap justify-between gap-6">
        <div className="bg-slate-900 p-4 rounded-lg w-full md:w-1/3">
          <h4 className="text-lg mb-2">Top Attack Types</h4>
          <Chart options={pieOptions} series={pieSeries} type="pie" width="100%" />
        </div>

        <div className="bg-slate-900 p-4 rounded-lg w-full md:w-2/3">
          <h4 className="text-lg mb-2">Attack Trend (Last 7 Days)</h4>
          <Chart options={trendOptions} series={trendSeries} type="line" width="100%" height={300} />
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-900 p-4 rounded-lg">
        <h4 className="text-lg mb-3">Top Attacking IPs</h4>
        <table className="w-full text-left text-slate-300">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="py-2">IP Address</th>
              <th className="py-2">Attack Count</th>
            </tr>
          </thead>
          <tbody>
            {data.top_ips.map((ip, i) => (
              <tr key={i} className="border-b border-slate-800">
                <td className="py-2">{ip.ip}</td>
                <td className="py-2">{ip.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AnalyticsDashboard
