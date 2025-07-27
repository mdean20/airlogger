import { Card, Badge } from "react-bootstrap";
import { format } from "date-fns";
import type { Flight } from "@/api/types";

interface FlightCardProps {
  flight: Flight;
  onViewDetails?: (flight: Flight) => void;
  variant?: "compact" | "full";
}

export function FlightCard({ flight, onViewDetails, variant = "compact" }: FlightCardProps) {
  return (
    <Card 
      className="flight-card" 
      onClick={() => onViewDetails?.(flight)}
      style={{ cursor: onViewDetails ? "pointer" : "default" }}
    >
      <Card.Body className={variant === "compact" ? "p-3" : "p-4"}>
        <div className="d-flex justify-content-between align-items-start">
          <div className="flex-grow-1">
            <h6 className="mb-1">
              {flight.departureAirport} → {flight.arrivalAirport}
            </h6>
            <p className="text-muted mb-0">
              <small>
                {format(new Date(flight.departureTime), "MMM d, h:mm a")} • {flight.billableHours} hrs
              </small>
            </p>
          </div>
          <Badge bg="success" className="ms-2">
            ${flight.estimatedRevenue.toFixed(2)}
          </Badge>
        </div>
        {variant === "full" && (
          <div className="mt-3 pt-3 border-top">
            <small className="text-muted">
              Hobbs Time: {flight.hobbsMinutes} min | 
              FlightAware: {flight.flightDurationMinutes} min |
              Tail: {flight.tailNumber}
            </small>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}