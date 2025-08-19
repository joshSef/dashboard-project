import { useEffect, useState } from "react";
import { fetchServices, type ServiceRow } from "./api";
import StatusDot from "./components/StatusDot";
import "./App.css";

function fmtDate(iso: string | null) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleString();
}

export default function App() {
  const [rows, setRows] = useState<ServiceRow[] | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data = await fetchServices();
        if (alive) setRows(data);
      } catch (e: any) {
        if (alive) setErr(e?.message ?? "Failed to load");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    const id = setInterval(async () => {
      try {
        const data = await fetchServices();
        if (alive) setRows(data);
      } catch (_) {}
    }, 5000); // refresh every 5s
    return () => {
      alive = false;
      clearInterval(id);
    };
  }, []);

return (
  <div style={{ maxWidth: 960, margin: "40px auto", padding: "0 16px" }}>
    <h1 style={{ marginBottom: 12 }}>Dashboard — Services</h1>
    <p style={{ marginTop: 0, color: "var(--muted)" }}>
      API: {import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}
    </p>

    {loading && <div>Loading…</div>}
    {err && (
      <div style={{ color: "var(--status-down)", marginBottom: 12 }}>
        Error: {err}. Is the API running on port 8000?
      </div>
    )}

    {rows && rows.length > 0 && (
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "separate", borderSpacing: 0 }}>
          <thead>
            <tr style={{ textAlign: "left", background: "var(--table-head-bg)" }}>
              {["Name", "Type", "Target", "Status", "Latency (ms)", "Last checked"].map((h) => (
                <th key={h} style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id}>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>{r.name}</td>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>{r.check_type}</td>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)", fontFamily: "monospace" }}>
                  {r.target}
                </td>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>
                  <StatusDot status={r.latest_status} />
                </td>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>
                  {r.latency_ms ?? "—"}
                </td>
                <td style={{ padding: "10px 12px", borderBottom: "1px solid var(--border)" }}>
                  {fmtDate(r.checked_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);
}
