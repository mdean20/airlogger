import { useQuery } from "@tanstack/react-query";
import { airloggerApi } from "@/api/endpoints";
import type { FlightParams } from "@/api/types";

export function useFlights(params?: FlightParams) {
  return useQuery({
    queryKey: ["flights", params],
    queryFn: () => airloggerApi.flights.list(params),
  });
}