export default function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-4">
      <div className="text-xs uppercase tracking-wide text-slate-400">{label}</div>
      <div className="text-2xl font-semibold mt-1">{value}</div>
    </div>
  )
}
