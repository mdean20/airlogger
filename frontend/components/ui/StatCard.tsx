import { Card } from "react-bootstrap";
import { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string | number;
  prefix?: string;
  suffix?: string;
  subtitle?: string;
  icon?: ReactNode;
  variant?: "primary" | "success" | "danger" | "warning" | "info";
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export function StatCard({
  title,
  value,
  prefix,
  suffix,
  subtitle,
  icon,
  variant = "primary",
  trend,
}: StatCardProps) {
  return (
    <Card className={`stat-card stat-card-${variant} h-100`}>
      <Card.Body>
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <p className="text-muted mb-1">{title}</p>
            <h3 className="mb-0">
              {prefix}
              {typeof value === "number" ? value.toLocaleString() : value}
              {suffix}
            </h3>
            {subtitle && (
              <small className="text-muted">{subtitle}</small>
            )}
            {trend && (
              <p className={`mb-0 mt-2 ${trend.isPositive ? "text-success" : "text-danger"}`}>
                <small>
                  {trend.isPositive ? "↑" : "↓"} {Math.abs(trend.value)}%
                </small>
              </p>
            )}
          </div>
          {icon && <div className="text-muted">{icon}</div>}
        </div>
      </Card.Body>
    </Card>
  );
}