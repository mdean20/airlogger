import axios from 'axios';
import { Flight, Summary, FinancialSettings } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const airloggerApi = {
  flights: {
    list: async (params?: { start_date?: string; end_date?: string }) => {
      const response = await api.get<Flight[]>('/flights', { params });
      return response.data;
    },
    refresh: async () => {
      const response = await api.post<{ message: string; flights_added: number }>('/refresh_data');
      return response.data;
    },
  },
  summary: {
    get: async (params?: { start_date?: string; end_date?: string }) => {
      const response = await api.get<Summary>('/summary', { params });
      return response.data;
    },
  },
  settings: {
    get: async () => {
      const response = await api.get<FinancialSettings>('/financial-settings');
      return response.data;
    },
    update: async (data: Partial<FinancialSettings>) => {
      const response = await api.put<FinancialSettings>('/financial-settings', data);
      return response.data;
    },
  },
};