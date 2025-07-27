'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { airloggerApi } from '@/lib/api';
import { Navigation } from '@/components/Navigation';
import { format, subDays } from 'date-fns';
import { RefreshCw, TrendingUp, DollarSign, Clock, Target } from 'lucide-react';

export default function Dashboard() {
  const queryClient = useQueryClient();
  
  const dateRange = {
    start_date: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
    end_date: format(new Date(), 'yyyy-MM-dd'),
  };

  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['summary', dateRange],
    queryFn: () => airloggerApi.summary.get(dateRange),
  });

  const { data: flights, isLoading: flightsLoading } = useQuery({
    queryKey: ['flights', dateRange],
    queryFn: () => airloggerApi.flights.list({ ...dateRange }),
  });

  const refreshMutation = useMutation({
    mutationFn: airloggerApi.flights.refresh,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['flights'] });
      queryClient.invalidateQueries({ queryKey: ['summary'] });
      alert(`Data refreshed! ${data.flights_added} new flights added.`);
    },
  });

  if (summaryLoading || flightsLoading) {
    return (
      <div>
        <Navigation />
        <div className="flex items-center justify-center h-screen">
          <div className="text-lg">Loading...</div>
        </div>
      </div>
    );
  }

  const recentFlights = flights?.slice(0, 5) || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={() => refreshMutation.mutate()}
            disabled={refreshMutation.isPending}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${refreshMutation.isPending ? 'animate-spin' : ''}`} />
            <span>{refreshMutation.isPending ? 'Refreshing...' : 'Refresh Data'}</span>
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Hours</p>
                <p className="text-2xl font-bold text-gray-900">
                  {summary?.totalBillableHours.toFixed(1) || '0'} hrs
                </p>
              </div>
              <Clock className="h-8 w-8 text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Revenue</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${summary?.totalRevenue.toLocaleString() || '0'}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Net Profit</p>
                <p className={`text-2xl font-bold ${
                  summary && summary.netProfit >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  ${summary?.netProfit.toLocaleString() || '0'}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-gray-600" />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">To Breakeven</p>
                <p className="text-2xl font-bold text-gray-900">
                  {summary?.breakeven.additionalHoursNeeded.toFixed(1) || '0'} hrs
                </p>
                <p className="text-xs text-gray-500">
                  ${summary?.breakeven.additionalRevenueNeeded.toLocaleString() || '0'}
                </p>
              </div>
              <Target className="h-8 w-8 text-orange-600" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Breakeven Progress */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Breakeven Progress</h2>
            {summary && (
              <div>
                <div className="mb-4">
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Progress</span>
                    <span className="text-sm font-medium text-gray-700">
                      {summary.breakeven.percentageToBreakeven.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-blue-600 h-4 rounded-full"
                      style={{
                        width: `${Math.min(summary.breakeven.percentageToBreakeven, 100)}%`,
                      }}
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Current Revenue</p>
                    <p className="font-semibold">${summary.breakeven.currentRevenue.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Breakeven Target</p>
                    <p className="font-semibold">${summary.breakeven.breakevenRevenue.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Recent Flights */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Recent Flights</h2>
              <a href="/flights" className="text-blue-600 hover:text-blue-800 text-sm">
                View All →
              </a>
            </div>
            
            {recentFlights.length > 0 ? (
              <div className="space-y-3">
                {recentFlights.map((flight) => (
                  <div key={flight.id} className="border rounded-lg p-3 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium">
                          {flight.departureAirport} → {flight.arrivalAirport}
                        </p>
                        <p className="text-sm text-gray-600">
                          {format(new Date(flight.departureTime), 'MMM d, h:mm a')} • 
                          {flight.billableHours.toFixed(1)} hrs
                        </p>
                      </div>
                      <span className="text-green-600 font-semibold">
                        ${flight.estimatedRevenue.toFixed(2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">No flights found</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}