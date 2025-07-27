# AirLogger Web Frontend Plan

A modern web application for aircraft flight tracking and financial analysis, built using the DCNTA platform technology stack.

## Technology Stack (Per AGENTS.md)

### Core Framework
- **Next.js 15.x** with App Router - Server-side rendering and routing
- **React 19.x** - UI component framework  
- **TypeScript 5.x** - Type safety and developer experience

### UI Framework
- **Bootstrap 5.3.x** - CSS framework for consistent styling
- **React Bootstrap 2.x** - React components for Bootstrap
- **SCSS** - Advanced styling with variables and mixins

### State Management
- **Zustand** - Global state for auth and app settings
- **TanStack Query** - Server state management for flight data
- **React Context** - Local component state (date ranges, filters)

### Data Fetching
- **Axios** - HTTP client with interceptors for AirLogger API
- **OpenAPI TypeScript** - Auto-generated types from backend API spec
- **React Use WebSocket** - Real-time flight updates (future feature)

## Application Structure

```
airlogger-web/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (dashboard)/       # Protected dashboard routes
│   │   │   ├── page.tsx       # Main dashboard
│   │   │   ├── flights/       # Flight history views
│   │   │   ├── analytics/     # Financial analytics
│   │   │   └── settings/      # App settings
│   │   ├── api/              # API proxy routes
│   │   └── auth/             # Authentication pages
│   ├── components/           # Reusable React components
│   │   ├── ui/              # Basic UI components
│   │   │   ├── DateRangePicker.tsx
│   │   │   ├── LoadingSkeleton.tsx
│   │   │   └── StatCard.tsx
│   │   ├── flights/         # Flight-specific components
│   │   │   ├── FlightCard.tsx
│   │   │   ├── FlightList.tsx
│   │   │   └── FlightTimeline.tsx
│   │   ├── analytics/       # Analytics components
│   │   │   ├── RevenueChart.tsx
│   │   │   ├── BreakevenGauge.tsx
│   │   │   └── SummaryCards.tsx
│   │   └── layout/          # Layout components
│   │       ├── Navigation.tsx
│   │       └── Footer.tsx
│   ├── hooks/               # Custom React hooks
│   │   ├── useFlights.ts
│   │   ├── useSummary.ts
│   │   └── useFinancialSettings.ts
│   ├── api/                 # API integration
│   │   ├── generated/       # Auto-generated from OpenAPI
│   │   ├── client.ts        # Axios client configuration
│   │   └── endpoints.ts     # API endpoint definitions
│   ├── stores/              # Zustand stores
│   │   ├── authStore.ts
│   │   ├── settingsStore.ts
│   │   └── filterStore.ts
│   └── styles/              # SCSS styles
│       ├── globals.scss
│       ├── variables.scss
│       └── components/
```

## Core Features & Components

### 1. Dashboard Overview
**Route**: `/`
- **Summary Cards**: Display key metrics (total hours, revenue, profit)
- **Recent Flights**: Last 5 flights with quick stats
- **Breakeven Progress**: Visual gauge showing progress to breakeven
- **Quick Actions**: Refresh data, change date range

### 2. Flight History
**Route**: `/flights`
- **Flight List**: Paginated table/cards of all flights
- **Filters**: Date range, airport codes, minimum duration
- **Flight Details**: Expandable rows with full flight information
- **Export**: Download as CSV/PDF

### 3. Financial Analytics
**Route**: `/analytics`
- **Revenue Chart**: Line/bar chart of revenue over time
- **Cost Breakdown**: Pie chart of fixed vs variable costs
- **Profit Trends**: Monthly/quarterly profit analysis
- **Breakeven Analysis**: Detailed breakeven calculations
- **What-if Scenarios**: Adjust rates to see impact

### 4. Settings
**Route**: `/settings`
- **Financial Parameters**: Update revenue/cost rates
- **Aircraft Settings**: Manage tail numbers (future)
- **API Configuration**: Backend URL settings
- **Export Settings**: Default export formats

## Component Design Patterns

### 1. Flight Card Component
```typescript
interface FlightCardProps {
  flight: Flight;
  onViewDetails?: (flight: Flight) => void;
  variant?: 'compact' | 'full';
}

export function FlightCard({ flight, onViewDetails, variant = 'compact' }: FlightCardProps) {
  return (
    <Card className="flight-card mb-3">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-start">
          <div>
            <h5>{flight.departureAirport} → {flight.arrivalAirport}</h5>
            <p className="text-muted">
              {formatDate(flight.departureTime)} • {flight.billableHours} hrs
            </p>
          </div>
          <Badge bg="success">${flight.estimatedRevenue}</Badge>
        </div>
        {variant === 'full' && (
          <div className="mt-3">
            <small className="text-muted">
              Hobbs Time: {flight.hobbsMinutes} min | 
              FlightAware: {flight.flightDurationMinutes} min
            </small>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}
```

### 2. Summary Dashboard
```typescript
export function DashboardSummary() {
  const { data: summary, isLoading } = useSummary();
  
  if (isLoading) return <DashboardSkeleton />;
  
  return (
    <Container>
      <Row className="g-4">
        <Col md={3}>
          <StatCard
            title="Total Hours"
            value={summary.totalBillableHours}
            suffix="hrs"
            icon={<Clock />}
          />
        </Col>
        <Col md={3}>
          <StatCard
            title="Revenue"
            value={summary.totalRevenue}
            prefix="$"
            trend={summary.revenueTrend}
          />
        </Col>
        <Col md={3}>
          <StatCard
            title="Net Profit"
            value={summary.netProfit}
            prefix="$"
            variant={summary.netProfit >= 0 ? 'success' : 'danger'}
          />
        </Col>
        <Col md={3}>
          <StatCard
            title="To Breakeven"
            value={summary.breakeven.additionalHoursNeeded}
            suffix="hrs"
            subtitle={`$${summary.breakeven.additionalRevenueNeeded}`}
          />
        </Col>
      </Row>
    </Container>
  );
}
```

### 3. API Integration
```typescript
// api/endpoints.ts
export const airloggerApi = {
  flights: {
    list: (params: FlightParams) => 
      client.get<Flight[]>('/flights', { params }),
    refresh: () => 
      client.post('/refresh_data'),
  },
  summary: {
    get: (params: SummaryParams) => 
      client.get<Summary>('/summary', { params }),
  },
  settings: {
    get: () => 
      client.get<FinancialSettings>('/financial-settings'),
    update: (data: FinancialSettings) => 
      client.put<FinancialSettings>('/financial-settings', data),
  },
};

// hooks/useFlights.ts
export function useFlights(filters: FlightFilters) {
  return useQuery({
    queryKey: ['flights', filters],
    queryFn: () => airloggerApi.flights.list(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

## UI/UX Design Principles

### 1. Mobile-First Responsive Design
- **Mobile**: Stack cards vertically, simplified navigation
- **Tablet**: 2-column layouts, collapsible sidebars
- **Desktop**: Full dashboard with multiple panels

### 2. Visual Hierarchy
- **Primary Actions**: Blue buttons for refresh, export
- **Success States**: Green for profit, completed flights
- **Warning States**: Orange for approaching limits
- **Danger States**: Red for losses, cancelled flights

### 3. Data Visualization
- **Charts**: Chart.js or Recharts for responsive graphs
- **Progress Indicators**: Bootstrap progress bars
- **Gauges**: Custom SVG components for breakeven
- **Tables**: React Table for sortable flight lists

### 4. Loading States
- **Skeleton Screens**: Show layout structure while loading
- **Progressive Loading**: Load summary first, then details
- **Optimistic Updates**: Update UI before API confirms

## Integration with DCNTA Platform

### 1. Authentication
```typescript
// Middleware checks auth state
export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    redirect('/auth/login');
  }
  
  return (
    <div className="dashboard-layout">
      <Navigation user={user} />
      <main className="container-fluid py-4">
        {children}
      </main>
    </div>
  );
}
```

### 2. Navigation Integration
```typescript
// Add AirLogger to DCNTA admin navigation
const navigationItems = [
  // ... existing items
  {
    label: 'AirLogger',
    icon: <Plane />,
    href: '/airlogger',
    subItems: [
      { label: 'Dashboard', href: '/airlogger' },
      { label: 'Flights', href: '/airlogger/flights' },
      { label: 'Analytics', href: '/airlogger/analytics' },
      { label: 'Settings', href: '/airlogger/settings' },
    ],
  },
];
```

### 3. Shared Components
- Use DCNTA's `ApiErrorFallback` for error handling
- Use DCNTA's `LoadingSkeleton` patterns
- Extend DCNTA's form components for settings

## Performance Optimizations

### 1. Data Caching Strategy
```typescript
// Aggressive caching for financial settings (rarely change)
queryClient.setQueryDefaults(['financial-settings'], {
  staleTime: 1000 * 60 * 60, // 1 hour
});

// Moderate caching for flight data
queryClient.setQueryDefaults(['flights'], {
  staleTime: 1000 * 60 * 5, // 5 minutes
});
```

### 2. Code Splitting
```typescript
// Lazy load heavy components
const AnalyticsCharts = dynamic(() => import('@/components/analytics/Charts'), {
  loading: () => <ChartSkeleton />,
});
```

### 3. Image Optimization
- Use Next.js Image for airport logos
- Lazy load flight timeline images
- WebP format for charts exports

## Testing Strategy

### 1. Component Tests
```typescript
describe('FlightCard', () => {
  it('displays flight information correctly', () => {
    const flight = mockFlight();
    render(<FlightCard flight={flight} />);
    
    expect(screen.getByText('KSFO → KLAX')).toBeInTheDocument();
    expect(screen.getByText('$299.00')).toBeInTheDocument();
  });
});
```

### 2. Integration Tests
```typescript
describe('Dashboard Integration', () => {
  it('loads and displays summary data', async () => {
    server.use(
      rest.get('/api/summary', (req, res, ctx) => {
        return res(ctx.json(mockSummary()));
      })
    );
    
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText('Total Hours')).toBeInTheDocument();
      expect(screen.getByText('2.1 hrs')).toBeInTheDocument();
    });
  });
});
```

## Deployment Configuration

### Environment Variables
```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_APP_NAME=AirLogger
NEXT_PUBLIC_DEFAULT_TAIL_NUMBER=N593EH
```

### Docker Configuration
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
RUN npm ci --production
EXPOSE 3000
CMD ["npm", "start"]
```

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live flight tracking
2. **Multiple Aircraft**: Support fleet management
3. **Weather Integration**: Show weather conditions for flights
4. **Maintenance Tracking**: Log maintenance hours and costs
5. **Mobile App**: React Native version for pilots
6. **PDF Reports**: Generate monthly/annual reports
7. **Notifications**: Alert when approaching breakeven
8. **Multi-tenant**: Support multiple operators

## Implementation Timeline

### Phase 1: Core Dashboard (Week 1)
- Basic layout and navigation
- Dashboard summary cards
- Flight list view
- Manual data refresh

### Phase 2: Analytics (Week 2)
- Revenue charts
- Cost breakdown
- Breakeven visualization
- Financial settings management

### Phase 3: Polish & Integration (Week 3)
- DCNTA platform integration
- Authentication flow
- Error handling
- Performance optimization

### Phase 4: Testing & Deployment (Week 4)
- Comprehensive testing
- Documentation
- Docker containerization
- Production deployment

---

This plan provides a comprehensive blueprint for building a modern, responsive web frontend for AirLogger that integrates seamlessly with the DCNTA platform while maintaining the high standards of code quality and user experience outlined in AGENTS.md.