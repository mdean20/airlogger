// API Types based on backend models

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
  createdAt: string;
}

export interface Summary {
  startDate: string;
  endDate: string;
  totalFlights: number;
  totalFlightMinutes: number;
  totalBillableHours: number;
  totalRevenue: number;
  totalVariableCosts: number;
  totalFixedCosts: number;
  netProfit: number;
  profitMargin: number;
  breakeven: {
    monthlyFixedCosts: number;
    variableCostPerHour: number;
    revenuePerHour: number;
    profitMarginPerHour: number;
    totalFixedCosts: number;
    breakevenHours: number;
    breakevenBillableHours: number;
    breakevenRevenue: number;
    currentHours: number;
    currentRevenue: number;
    additionalHoursNeeded: number;
    additionalRevenueNeeded: number;
    percentageToBreakeven: number;
  };
}

export interface FinancialSettings {
  id: number;
  revenue_per_hour: number;
  monthly_fixed_costs: number;
  variable_cost_per_hour: number;
  updated_at: string;
}

// Query Parameters
export interface FlightParams {
  start_date?: string;
  end_date?: string;
  limit?: number;
}

export interface SummaryParams {
  start_date?: string;
  end_date?: string;
}