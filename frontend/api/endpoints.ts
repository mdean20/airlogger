import { client } from "./client";
import type {
  Flight,
  Summary,
  FinancialSettings,
  FlightParams,
  SummaryParams,
} from "./types";

export const airloggerApi = {
  flights: {
    list: (params?: FlightParams) =>
      client.get<Flight[]>("/flights", { params }).then((res) => res.data),
    refresh: () =>
      client.post<{ message: string; flights_added: number }>("/refresh_data").then((res) => res.data),
  },
  summary: {
    get: (params?: SummaryParams) =>
      client.get<Summary>("/summary", { params }).then((res) => res.data),
  },
  settings: {
    get: () =>
      client.get<FinancialSettings>("/financial-settings").then((res) => res.data),
    update: (data: Partial<FinancialSettings>) =>
      client.put<FinancialSettings>("/financial-settings", data).then((res) => res.data),
  },
};