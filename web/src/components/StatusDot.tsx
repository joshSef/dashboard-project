type Props = { status: "UP" | "DOWN" | null | undefined };

export default function StatusDot({ status }: Props) {
  let color = "var(--status-unknown)";
  if (status === "UP") color = "var(--status-up)";
  if (status === "DOWN") color = "var(--status-down)";
  const label = status ?? "UNKNOWN";
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
      <span
        aria-label={label}
        title={label}
        style={{
          width: 10,
          height: 10,
          borderRadius: "9999px",
          background: color,
          display: "inline-block",
        }}
      />
      <span style={{ fontSize: 12, color: "var(--muted)" }}>{label}</span>
    </span>
  );
}
