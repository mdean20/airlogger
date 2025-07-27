import { useQuery } from "@tanstack/react-query";
import { airloggerApi } from "@/api/endpoints";
import type { SummaryParams } from "@/api/types";

export function useSummary(params?: SummaryParams) {
  return useQuery({
    queryKey: ["summary", params],
    queryFn: () => airloggerApi.summary.get(params),
  });
}