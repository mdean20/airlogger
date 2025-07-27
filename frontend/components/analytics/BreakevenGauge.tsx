import { ProgressBar } from "react-bootstrap";
import type { Summary } from "@/api/types";

interface BreakevenGaugeProps {
  summary: Summary;
}

export function BreakevenGauge({ summary }: BreakevenGaugeProps) {
  const { breakeven } = summary;
  const percentage = Math.min(breakeven.percentageToBreakeven, 100);

  return (
    <div>
      <div className="d-flex justify-content-between mb-2">
        <span>Progress to Breakeven</span>
        <span className="fw-bold">{percentage.toFixed(1)}%</span>
      </div>
      
      <ProgressBar 
        now={percentage} 
        variant={percentage >= 100 ? "success" : percentage >= 75 ? "warning" : "primary"}
        style={{ height: "2rem" }}
      />
      
      <div className="row mt-4">
        <div className="col-6">
          <p className="mb-1 text-muted">Current Revenue</p>
          <h5>${breakeven.currentRevenue.toLocaleString()}</h5>
        </div>
        <div className="col-6">
          <p className="mb-1 text-muted">Breakeven Target</p>
          <h5>${breakeven.breakevenRevenue.toLocaleString()}</h5>
        </div>
      </div>
      
      <div className="row mt-3">
        <div className="col-6">
          <p className="mb-1 text-muted">Hours Flown</p>
          <h5>{breakeven.currentHours.toFixed(1)} hrs</h5>
        </div>
        <div className="col-6">
          <p className="mb-1 text-muted">Hours Needed</p>
          <h5>{breakeven.additionalHoursNeeded.toFixed(1)} hrs</h5>
        </div>
      </div>

      <div className="mt-4 p-3 bg-light rounded">
        <small className="text-muted">
          <strong>Monthly Fixed Costs:</strong> ${breakeven.monthlyFixedCosts.toLocaleString()} | 
          <strong> Revenue/Hour:</strong> ${breakeven.revenuePerHour} | 
          <strong> Variable Cost/Hour:</strong> ${breakeven.variableCostPerHour}
        </small>
      </div>
    </div>
  );
}