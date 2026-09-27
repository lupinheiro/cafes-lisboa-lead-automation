import type { DashboardMetrics } from "../api/hooks";

export function MetricsCards({ metrics }: { metrics: DashboardMetrics }) {
  const cards = [
    { label: "Total de leads", value: metrics.total_leads },
    { label: "Pendentes de revisão", value: metrics.pending_review },
    { label: "Enviados", value: metrics.sent },
    { label: "Pontuação média", value: metrics.average_score },
  ];

  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
      {cards.map((card) => (
        <div key={card.label} className="rounded-lg border border-gray-200 p-4">
          <p className="text-sm text-gray-500">{card.label}</p>
          <p className="text-2xl font-semibold">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
