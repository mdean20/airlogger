'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { airloggerApi } from '@/lib/api';
import { Navigation } from '@/components/Navigation';
import { useState, useEffect } from 'react';
import { Save, DollarSign, TrendingDown, Calendar } from 'lucide-react';

export default function SettingsPage() {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    revenue_per_hour: 0,
    monthly_fixed_costs: 0,
    variable_cost_per_hour: 0,
  });

  const { data: settings, isLoading } = useQuery({
    queryKey: ['financial-settings'],
    queryFn: airloggerApi.settings.get,
  });

  useEffect(() => {
    if (settings) {
      setFormData({
        revenue_per_hour: settings.revenue_per_hour,
        monthly_fixed_costs: settings.monthly_fixed_costs,
        variable_cost_per_hour: settings.variable_cost_per_hour,
      });
    }
  }, [settings]);

  const updateMutation = useMutation({
    mutationFn: airloggerApi.settings.update,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['financial-settings'] });
      queryClient.invalidateQueries({ queryKey: ['summary'] });
      alert('Settings updated successfully!');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }));
  };

  if (isLoading) {
    return (
      <div>
        <Navigation />
        <div className="flex items-center justify-center h-screen">
          <div className="text-lg">Loading settings...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Financial Settings</h1>
        
        <div className="max-w-2xl">
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6">
            <div className="space-y-6">
              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <DollarSign className="h-4 w-4 mr-2" />
                  Revenue per Hour
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
                  <input
                    type="number"
                    name="revenue_per_hour"
                    value={formData.revenue_per_hour}
                    onChange={handleChange}
                    step="0.01"
                    className="pl-8 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Amount charged per billable flight hour
                </p>
              </div>

              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <Calendar className="h-4 w-4 mr-2" />
                  Monthly Fixed Costs
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
                  <input
                    type="number"
                    name="monthly_fixed_costs"
                    value={formData.monthly_fixed_costs}
                    onChange={handleChange}
                    step="0.01"
                    className="pl-8 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Fixed monthly costs (hangar, insurance, etc.)
                </p>
              </div>

              <div>
                <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                  <TrendingDown className="h-4 w-4 mr-2" />
                  Variable Cost per Hour
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
                  <input
                    type="number"
                    name="variable_cost_per_hour"
                    value={formData.variable_cost_per_hour}
                    onChange={handleChange}
                    step="0.01"
                    className="pl-8 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <p className="mt-1 text-sm text-gray-500">
                  Variable costs per flight hour (fuel, maintenance reserves)
                </p>
              </div>
            </div>

            <div className="mt-6 border-t pt-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Calculations</h3>
                <div className="space-y-1 text-sm text-gray-600">
                  <p>
                    Profit Margin per Hour: <span className="font-medium">
                      ${(formData.revenue_per_hour - formData.variable_cost_per_hour).toFixed(2)}
                    </span>
                  </p>
                  <p>
                    Hours to Cover Monthly Fixed Costs: <span className="font-medium">
                      {formData.revenue_per_hour - formData.variable_cost_per_hour > 0
                        ? (formData.monthly_fixed_costs / (formData.revenue_per_hour - formData.variable_cost_per_hour)).toFixed(1)
                        : '∞'} hrs
                    </span>
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <button
                type="submit"
                disabled={updateMutation.isPending}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                <Save className="h-4 w-4" />
                <span>{updateMutation.isPending ? 'Saving...' : 'Save Settings'}</span>
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}