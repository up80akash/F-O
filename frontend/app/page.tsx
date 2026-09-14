export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="mx-auto max-w-6xl rounded-2xl border border-slate-700 bg-slate-900 p-8 shadow-2xl">
        <div className="mb-6 flex items-center justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-cyan-400">Market terminal</p>
            <h1 className="mt-2 text-3xl font-bold text-white">F&O Trading Platform</h1>
          </div>
          <div className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-300">
            PAPER MODE
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <StatusCard label="Market" value="NIFTY" tone="cyan" />
          <StatusCard label="Trend" value="BULLISH" tone="emerald" />
          <StatusCard label="AI" value="ONLINE" tone="violet" />
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <div className="rounded-xl border border-slate-700 bg-slate-950 p-4">
            <h2 className="mb-3 text-lg font-semibold text-slate-100">System status</h2>
            <ul className="space-y-2 text-sm text-slate-300">
              <li>• API: HEALTHY</li>
              <li>• Database: READY</li>
              <li>• Redis: READY</li>
              <li>• Broker: DISCONNECTED</li>
            </ul>
          </div>
          <div className="rounded-xl border border-slate-700 bg-slate-950 p-4">
            <h2 className="mb-3 text-lg font-semibold text-slate-100">Phase 1</h2>
            <ul className="space-y-2 text-sm text-slate-300">
              <li>• Docker scaffolded</li>
              <li>• Backend bootstrapped</li>
              <li>• Frontend bootstrapped</li>
              <li>• Docs and env config ready</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}

function StatusCard({ label, value, tone }: { label: string; value: string; tone: string }) {
  const toneMap: Record<string, string> = {
    cyan: "border-cyan-500/30 bg-cyan-500/10 text-cyan-300",
    emerald: "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
    violet: "border-violet-500/30 bg-violet-500/10 text-violet-300",
  };

  return (
    <div className={`rounded-xl border p-4 ${toneMap[tone]}`}>
      <p className="text-xs uppercase tracking-[0.2em] opacity-80">{label}</p>
      <p className="mt-3 text-2xl font-bold">{value}</p>
    </div>
  );
}
