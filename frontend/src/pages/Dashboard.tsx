import { useDashboardMetrics, useLeads } from "../api/hooks";
import { LeadsTable } from "../components/LeadsTable";
import { MetricsCards } from "../components/MetricsCards";
import { StatusChart } from "../components/StatusChart";

export function Dashboard() {
  const metricsQuery = useDashboardMetrics();
  const leadsQuery = useLeads();

  if (metricsQuery.isLoading || leadsQuery.isLoading) {
    return <p className="p-6">A carregar...</p>;
  }

  if (metricsQuery.isError || leadsQuery.isError || !metricsQuery.data || !leadsQuery.data) {
    return <p className="p-6 text-red-600">Erro ao carregar dados da API.</p>;
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6 p-6">
      <h1 className="text-xl font-medium">Prospeção Cafés Lisboa</h1>
      <MetricsCards metrics={metricsQuery.data} />
      <StatusChart byStatus={metricsQuery.data.by_status} />
      <LeadsTable leads={leadsQuery.data} />
    </div>
  );
}
