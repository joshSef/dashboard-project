type Props = { status: "UP" | "DOWN" | null | undefined };

export default function StatusDot({ status }: Props) {
  const color = status === "UP" ? "#22c55e" : status === "DOWN" ? "#ef4444" : "#9ca3af";
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
      <span style={{ fontSize: 12, color: "#4b5563" }}>{label}</span>
    </span>
  );
}
