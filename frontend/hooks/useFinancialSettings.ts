import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { airloggerApi } from "@/api/endpoints";
import type { FinancialSettings } from "@/api/types";

export function useFinancialSettings() {
  return useQuery({
    queryKey: ["financial-settings"],
    queryFn: airloggerApi.settings.get,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

export function useUpdateFinancialSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<FinancialSettings>) => airloggerApi.settings.update(data),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ["financial-settings"] });
      queryClient.invalidateQueries({ queryKey: ["summary"] });
    },
  });
}