# AGENTS.md - Frontend Architecture Guide for Developer Applications

This document provides architectural guidance for developers building frontend applications that integrate with the DCNTA platform. It outlines the technology stack, architectural patterns, and decision records to ensure low-friction integration of additional developer applications.

## Technology Stack

### Core Framework
- **Next.js 15.x** with App Router - Server-side rendering and routing
- **React 19.x** - UI component framework
- **TypeScript 5.x** - Type safety and developer experience

### UI Framework
- **Bootstrap 5.3.x** - CSS framework for consistent styling
- **React Bootstrap 2.x** - React components for Bootstrap
- **SCSS** - Advanced styling with variables and mixins

### State Management
- **Zustand** - Lightweight state management for auth and global state
- **TanStack Query (React Query)** - Server state management and caching
- **React Context** - Local component state sharing

### Data Fetching
- **Axios** - HTTP client with interceptors
- **OpenAPI TypeScript** - Auto-generated types from API specifications
- **React Use WebSocket** - Real-time data connections

### Development Tools
- **Jest & Testing Library** - Unit and integration testing
- **MSW (Mock Service Worker)** - API mocking for tests
- **Puppeteer** - E2E testing
- **ESLint & Prettier** - Code quality and formatting

## Architectural Patterns

### 1. API-First Development
All frontend applications must be designed as consumers of backend APIs:
- No business logic in frontend
- All data processing handled by backend services
- Frontend focuses on presentation and user interaction

### 2. Type-Safe API Integration
Use auto-generated TypeScript types from OpenAPI specifications:
```typescript
// Auto-generated from OpenAPI spec
import { api } from '@/api/typed-client';
import type { Device, DeviceResponse } from '@/api/generated/openapi';

// Type-safe API calls
const devices = await api.devices.list({ page: 1, limit: 20 });
```

### 3. Centralized Error Handling
Implement consistent error handling across all applications:
```typescript
// Use the ApiErrorFallback component
<ApiErrorFallback 
  error={error} 
  retry={() => refetch()}
/>

// Use the useApiCall hook
const { execute, loading, error } = useApiCall(api.devices.create);
```

### 4. Authentication Pattern
All applications must use the centralized authentication system:
```typescript
// Authentication is handled by middleware
// Access auth state via Zustand store
const { user, isAuthenticated } = useAuthStore();
```

### 5. Real-time Data Pattern
For applications requiring real-time updates:
```typescript
// Use the WebSocket hook
const { data, error } = useWebSocketV2('/telemetry/stream');
```

## Architectural Decision Records (ADRs)

### ADR-001: Next.js App Router
**Status**: Accepted  
**Decision**: Use Next.js 15 App Router for all new applications  
**Rationale**: 
- Server-side rendering for better performance
- Built-in routing with layouts
- Streaming and suspense support
- Better SEO capabilities

### ADR-002: TypeScript Strict Mode
**Status**: Accepted  
**Decision**: All code must be written in TypeScript with strict mode enabled  
**Rationale**:
- Catch errors at compile time
- Better IDE support and autocompletion
- Self-documenting code
- Easier refactoring

### ADR-003: Bootstrap Design System
**Status**: Accepted  
**Decision**: Use Bootstrap 5 as the base design system  
**Rationale**:
- Consistent UI across all applications
- Extensive component library
- Responsive by default
- Well-documented and maintained

### ADR-004: API Contract Testing
**Status**: Accepted  
**Decision**: All API integrations must be validated against OpenAPI specifications  
**Rationale**:
- Ensure frontend-backend compatibility
- Catch breaking changes early
- Auto-generate TypeScript types
- Document API usage

### ADR-005: Component-Based Architecture
**Status**: Accepted  
**Decision**: Build applications using small, reusable components  
**Rationale**:
- Better code organization
- Easier testing
- Component reusability
- Parallel development

### ADR-006: Error Boundaries
**Status**: Accepted  
**Decision**: Implement error boundaries for graceful error handling  
**Rationale**:
- Prevent entire app crashes
- Better user experience
- Centralized error logging
- Easier debugging

### ADR-007: Progressive Enhancement
**Status**: Accepted  
**Decision**: Build features that work without JavaScript, enhance with JS  
**Rationale**:
- Better accessibility
- Faster initial page loads
- SEO benefits
- Graceful degradation

### ADR-008: Test-Driven Development
**Status**: Accepted  
**Decision**: Write tests before implementing features  
**Rationale**:
- Better code quality
- Fewer bugs in production
- Living documentation
- Confident refactoring

## Application Structure

### Directory Layout
```
src/
├── app/                    # Next.js App Router pages
│   ├── (admin)/           # Protected admin routes
│   ├── api/               # API routes
│   └── auth/              # Authentication pages
├── components/            # Reusable React components
│   ├── ui/               # Basic UI components
│   ├── forms/            # Form components
│   └── [feature]/        # Feature-specific components
├── hooks/                 # Custom React hooks
├── lib/                   # Utility libraries
├── api/                   # API integration
│   ├── generated/         # Auto-generated types
│   └── typed-client.ts    # Type-safe API client
├── context/              # React contexts
├── assets/               # Static assets
└── types/                # TypeScript type definitions
```

### Component Guidelines

#### 1. Component Structure
```typescript
// components/devices/DeviceCard.tsx
interface DeviceCardProps {
  device: Device;
  onEdit?: (device: Device) => void;
  onDelete?: (device: Device) => void;
}

export function DeviceCard({ device, onEdit, onDelete }: DeviceCardProps) {
  // Component logic
}
```

#### 2. Error Handling
```typescript
// Always handle loading and error states
if (isLoading) return <LoadingSkeleton />;
if (error) return <ApiErrorFallback error={error} retry={refetch} />;
```

#### 3. Data Fetching
```typescript
// Use TanStack Query for data fetching
const { data, isLoading, error } = useQuery({
  queryKey: ['devices', filters],
  queryFn: () => api.devices.list(filters),
});
```

## Integration Guidelines

### 1. API Integration Checklist
- [ ] Generate TypeScript types from OpenAPI spec
- [ ] Implement error handling for all API calls
- [ ] Add loading states for async operations
- [ ] Handle authentication errors (401)
- [ ] Implement retry logic for failed requests

### 2. UI Integration Checklist
- [ ] Follow Bootstrap design patterns
- [ ] Implement responsive layouts
- [ ] Add loading skeletons
- [ ] Include error boundaries
- [ ] Test on multiple screen sizes

### 3. State Management Checklist
- [ ] Use Zustand for global state
- [ ] Use TanStack Query for server state
- [ ] Implement optimistic updates where appropriate
- [ ] Handle stale data scenarios

### 4. Testing Checklist
- [ ] Write unit tests for components
- [ ] Add integration tests for API calls
- [ ] Include error scenario tests
- [ ] Test loading states
- [ ] Verify accessibility

## Common Patterns

### API Error Handling
```typescript
const { execute, loading, error } = useApiCall(
  api.devices.create,
  {
    onSuccess: (data) => {
      toast.success('Device created successfully');
      router.push(`/devices/${data.id}`);
    },
    onError: (error) => {
      // Error is automatically shown via toast
      console.error('Failed to create device:', error);
    }
  }
);
```

### Form Handling
```typescript
const { register, handleSubmit, formState: { errors } } = useForm<DeviceForm>({
  resolver: yupResolver(deviceSchema),
});

const onSubmit = async (data: DeviceForm) => {
  await execute(data);
};
```

### Real-time Updates
```typescript
const { data: telemetry } = useWebSocketV2('/telemetry/stream', {
  onMessage: (data) => {
    // Update local state with new telemetry data
    updateTelemetryStore(data);
  },
});
```

## Performance Guidelines

1. **Code Splitting**: Use dynamic imports for large components
2. **Image Optimization**: Use Next.js Image component
3. **Bundle Size**: Monitor and optimize bundle sizes
4. **Caching**: Implement proper cache strategies with TanStack Query
5. **Lazy Loading**: Defer loading of non-critical components

## Security Guidelines

1. **Authentication**: Always verify authentication state
2. **Authorization**: Check permissions before showing UI elements
3. **Input Validation**: Validate all user inputs
4. **XSS Prevention**: Use React's built-in XSS protection
5. **Secure Storage**: Never store sensitive data in localStorage

## Deployment

All applications follow the same deployment pipeline:
1. Push to `staging` branch
2. Automated tests run via GitHub Actions
3. Deploy to staging environment
4. After verification, merge to `main`
5. Automated deployment to production

## Getting Started

For new developers:
1. Clone the repository
2. Copy `.env.example` to `.env.local`
3. Run `npm install`
4. Run `npm run dev`
5. Access the app at `http://localhost:3000`

## Contributing

1. Create a feature branch from `staging`
2. Follow TDD - write tests first
3. Ensure all tests pass
4. Create a pull request to `staging`
5. After review and staging deployment, merge to `main`

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Bootstrap Components](https://react-bootstrap.github.io/)
- [TanStack Query Documentation](https://tanstack.com/query)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/)

---

This architecture ensures that all developer applications integrate seamlessly with the DCNTA platform while maintaining consistency, type safety, and excellent user experience.