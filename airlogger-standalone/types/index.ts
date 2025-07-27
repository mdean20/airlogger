export interface Flight {
  id: string;
  tailNumber: string;
  departureAirport: string;
  arrivalAirport: string;
  departureTime: string;
  arrivalTime: string;
  flightDurationMinutes: number;
  hobbsMinutes: number;
  billableHours: number;
  estimatedRevenue: number;
}

export interface Summary {
  totalFlights: number;
  totalBillableHours: number;
  totalRevenue: number;
  totalVariableCosts: number;
  totalFixedCosts: number;
  netProfit: number;
  breakeven: {
    additionalHoursNeeded: number;
    additionalRevenueNeeded: number;
    percentageToBreakeven: number;
    currentRevenue: number;
    breakevenRevenue: number;
  };
}

export interface FinancialSettings {
  id: number;
  revenue_per_hour: number;
  monthly_fixed_costs: number;
  variable_cost_per_hour: number;
}