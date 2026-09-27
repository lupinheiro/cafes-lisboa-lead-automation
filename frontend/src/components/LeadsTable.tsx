import { useReviewLead } from "../api/hooks";
import type { Lead } from "../api/hooks";

export function LeadsTable({ leads }: { leads: Lead[] }) {
  const reviewLead = useReviewLead();

  return (
    <table className="w-full border-collapse text-sm">
      <thead>
        <tr className="border-b border-gray-200 text-left text-gray-500">
          <th className="py-2">Nome</th>
          <th className="py-2">Tipo</th>
          <th className="py-2">Score</th>
          <th className="py-2">Estado</th>
          <th className="py-2">Ação</th>
        </tr>
      </thead>
      <tbody>
        {leads.map((lead) => (
          <tr key={lead.id} className="border-b border-gray-100">
            <td className="py-2">{lead.name}</td>
            <td className="py-2">{lead.business_type}</td>
            <td className="py-2">{lead.score.toFixed(1)}</td>
            <td className="py-2">{lead.status}</td>
            <td className="py-2">
              {lead.status === "pending_review" && (
                <div className="flex gap-2">
                  <button
                    className="rounded bg-emerald-600 px-2 py-1 text-white"
                    onClick={() => reviewLead.mutate({ leadId: lead.id, approved: true })}
                  >
                    Aprovar
                  </button>
                  <button
                    className="rounded bg-gray-200 px-2 py-1"
                    onClick={() => reviewLead.mutate({ leadId: lead.id, approved: false })}
                  >
                    Rejeitar
                  </button>
                </div>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
