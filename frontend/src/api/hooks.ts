import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { apiClient } from "./client";

export interface Lead {
  id: string;
  name: string;
  business_type: string;
  address: string | null;
  score: number;
  status: string;
  outreach_draft: string | null;
}

export interface DashboardMetrics {
  total_leads: number;
  by_status: Record<string, number>;
  average_score: number;
  pending_review: number;
  sent: number;
}

export function useLeads(status?: string) {
  return useQuery({
    queryKey: ["leads", status],
    queryFn: async () => {
      const { data } = await apiClient.get<Lead[]>("/leads", {
        params: status ? { status } : undefined,
      });
      return data;
    },
    refetchInterval: 30_000,
  });
}

export function useDashboardMetrics() {
  return useQuery({
    queryKey: ["dashboard-metrics"],
    queryFn: async () => {
      const { data } = await apiClient.get<DashboardMetrics>("/dashboard/metrics");
      return data;
    },
    refetchInterval: 30_000,
  });
}

export function useReviewLead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ leadId, approved }: { leadId: string; approved: boolean }) => {
      const { data } = await apiClient.post(`/leads/${leadId}/review`, { approved });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["leads"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-metrics"] });
    },
  });
}
