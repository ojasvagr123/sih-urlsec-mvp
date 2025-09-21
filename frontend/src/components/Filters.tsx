import { useState } from "react"

type Props = {
  onApply: (q: { attack_type?: string; ip?: string; success?: string }) => void
}

export default function Filters({ onApply }: Props) {
  const [attackType, setAttackType] = useState("")
  const [ip, setIp] = useState("")
  const [success, setSuccess] = useState("")

  return (
    <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-4 mb-4">
      <div className="flex flex-wrap items-end gap-3">
        <div>
          <label className="block text-sm text-slate-300">Attack type</label>
          <input
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm"
            placeholder="e.g. sql_injection"
            value={attackType}
            onChange={(e) => setAttackType(e.target.value)}
          />
        </div>
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
          <label className="block text-sm text-slate-300">Success</label>
          <select
            className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm"
            value={success}
            onChange={(e) => setSuccess(e.target.value)}
          >
            <option value="">Any</option>
            <option value="true">True</option>
            <option value="false">False</option>
          </select>
        </div>
        <button
          className="ml-auto bg-blue-600 hover:bg-blue-500 transition text-white px-3 py-2 rounded"
          onClick={() => onApply({ attack_type: attackType || undefined, ip: ip || undefined, success: success || undefined })}
        >
          Apply
        </button>
      </div>
    </div>
  )
}
