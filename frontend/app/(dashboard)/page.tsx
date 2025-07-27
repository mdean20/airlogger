"use client";

import { Container, Row, Col, Card, Button } from "react-bootstrap";
import { useSummary, useFlights } from "@/hooks";
import { StatCard } from "@/components/ui/StatCard";
import { DashboardSkeleton } from "@/components/ui/LoadingSkeleton";
import { FlightCard } from "@/components/flights/FlightCard";
import { BreakevenGauge } from "@/components/analytics/BreakevenGauge";
import { format, subDays } from "date-fns";
import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { airloggerApi } from "@/api/endpoints";

export default function DashboardPage() {
  const [dateRange] = useState({
    start_date: format(subDays(new Date(), 30), "yyyy-MM-dd"),
    end_date: format(new Date(), "yyyy-MM-dd"),
  });

  const { data: summary, isLoading: summaryLoading } = useSummary(dateRange);
  const { data: flights, isLoading: flightsLoading } = useFlights({
    ...dateRange,
    limit: 5,
  });

  const queryClient = useQueryClient();
  const refreshMutation = useMutation({
    mutationFn: airloggerApi.flights.refresh,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["flights"] });
      queryClient.invalidateQueries({ queryKey: ["summary"] });
      alert(`Data refreshed! ${data.flights_added} new flights added.`);
    },
  });

  if (summaryLoading || flightsLoading) {
    return <DashboardSkeleton />;
  }

  return (
    <Container className="py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard</h1>
        <Button
          variant="primary"
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
        >
          {refreshMutation.isPending ? "Refreshing..." : "Refresh Data"}
        </Button>
      </div>

      {/* Summary Cards */}
      <Row className="g-4 mb-4">
        <Col md={6} lg={3}>
          <StatCard
            title="Total Hours"
            value={summary?.totalBillableHours || 0}
            suffix=" hrs"
            variant="primary"
          />
        </Col>
        <Col md={6} lg={3}>
          <StatCard
            title="Revenue"
            value={summary?.totalRevenue || 0}
            prefix="$"
            variant="info"
          />
        </Col>
        <Col md={6} lg={3}>
          <StatCard
            title="Net Profit"
            value={summary?.netProfit || 0}
            prefix="$"
            variant={summary && summary.netProfit >= 0 ? "success" : "danger"}
          />
        </Col>
        <Col md={6} lg={3}>
          <StatCard
            title="To Breakeven"
            value={summary?.breakeven.additionalHoursNeeded || 0}
            suffix=" hrs"
            subtitle={`$${summary?.breakeven.additionalRevenueNeeded.toLocaleString() || 0}`}
            variant="warning"
          />
        </Col>
      </Row>

      <Row className="g-4">
        {/* Breakeven Progress */}
        <Col lg={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Breakeven Progress</h5>
            </Card.Header>
            <Card.Body>
              {summary && <BreakevenGauge summary={summary} />}
            </Card.Body>
          </Card>
        </Col>

        {/* Recent Flights */}
        <Col lg={4}>
          <Card>
            <Card.Header className="d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Recent Flights</h5>
              <Button variant="link" size="sm" href="/flights">
                View All
              </Button>
            </Card.Header>
            <Card.Body>
              {flights && flights.length > 0 ? (
                <div className="d-flex flex-column gap-3">
                  {flights.map((flight) => (
                    <FlightCard key={flight.id} flight={flight} variant="compact" />
                  ))}
                </div>
              ) : (
                <p className="text-muted text-center">No flights found</p>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}