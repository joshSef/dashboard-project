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
      <p style={{ marginTop: 0, color: "#6b7280" }}>
        API: {import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}
      </p>

      {loading && <div>Loading…</div>}
      {err && (
        <div style={{ color: "#ef4444", marginBottom: 12 }}>
          Error: {err}. Is the API running on port 8000?
        </div>
      )}

      {rows && rows.length === 0 && <div>No services found.</div>}

      {rows && rows.length > 0 && (
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "separate", borderSpacing: 0 }}>
            <thead>
              <tr style={{ textAlign: "left", background: "#f9fafb" }}>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Name</th>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Type</th>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Target</th>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Status</th>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Latency (ms)</th>
                <th style={{ padding: "10px 12px", borderBottom: "1px solid #e5e7eb" }}>Last checked</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>{r.name}</td>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>{r.check_type}</td>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6", fontFamily: "monospace" }}>
                    {r.target}
                  </td>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>
                    <StatusDot status={r.latest_status} />
                  </td>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>
                    {r.latency_ms ?? "—"}
                  </td>
                  <td style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>
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
