const BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export type ServiceRow = {
  id: number;
  name: string;
  check_type: "HTTP" | "TCP";
  target: string;
  latest_status: "UP" | "DOWN" | null;
  latency_ms: number | null;
  checked_at: string | null;
};

export async function fetchServices(): Promise<ServiceRow[]> {
  const res = await fetch(`${BASE}/api/services`);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
