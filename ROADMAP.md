# Aircraft Tracking Application Roadmap

## Project Overview
Personal aircraft tracking and flight time logging application for N593EH, with M2 Mac backend and iOS frontend.

## Current Status: 🚧 Initial Development

### Architecture Summary
- **Backend**: Python Flask API on M2 Mac Mini
- **Frontend**: iOS SwiftUI application
- **Database**: SQLite (local)
- **Connectivity**: Tailscale VPN
- **Data Source**: FlightAware AeroAPI

## Development Phases

### Phase 1: Core Backend Development ⏳
**Status**: Not Started
**Priority**: Critical

#### Tasks:
- [ ] Set up Python Flask project structure
- [ ] Create requirements.txt with dependencies
- [ ] Implement FlightAware AeroAPI integration
  - [ ] Environment variable configuration (.env)
  - [ ] API authentication
  - [ ] Flight data fetching for N593EH
- [ ] Set up SQLite database with SQLAlchemy
  - [ ] Create FlightRecord model
  - [ ] Database initialization
- [ ] Implement core API endpoints:
  - [ ] POST /api/refresh_data
  - [ ] GET /api/flights
  - [ ] GET /api/summary
- [ ] Add error handling and logging
- [ ] Test API endpoints manually

#### Dependencies:
- FlightAware API key
- Python 3.x environment
- Flask, SQLAlchemy, requests libraries

### Phase 2: iOS Application Foundation ⏳
**Status**: Not Started
**Priority**: High

#### Tasks:
- [ ] Create new iOS project in Xcode
- [ ] Set up SwiftUI project structure
- [ ] Create data models (Flight, Summary)
- [ ] Implement BackendService class
  - [ ] URLSession configuration
  - [ ] API endpoint methods
  - [ ] Error handling
- [ ] Design main dashboard view
- [ ] Implement date picker controls
- [ ] Create flight list view
- [ ] Add loading states and error handling

#### Dependencies:
- Backend API running and accessible
- Tailscale configured on iOS device
- Xcode development environment

### Phase 3: Connectivity & Integration ⏳
**Status**: Not Started
**Priority**: High

#### Tasks:
- [ ] Install Tailscale on M2 Mac Mini
- [ ] Install Tailscale on iOS device
- [ ] Configure Tailscale network
- [ ] Test connectivity between devices
- [ ] Update iOS app with correct backend URL
- [ ] Test end-to-end data flow

#### Dependencies:
- Tailscale account
- Both Phase 1 and Phase 2 complete

### Phase 4: Financial Features ⏳
**Status**: Not Started
**Priority**: Medium

#### Tasks:
- [ ] Implement financial calculations in backend
  - [ ] Revenue per hour calculations
  - [ ] Fixed costs (monthly insurance)
  - [ ] Variable costs (fuel, oil per hour)
- [ ] Create iOS settings view
  - [ ] Input fields for financial parameters
  - [ ] Local storage of settings
- [ ] Update API to accept financial parameters
- [ ] Display revenue/cost summaries in iOS app

#### Dependencies:
- Core functionality working (Phases 1-3)

### Phase 5: Data Management & Optimization ⏳
**Status**: Not Started
**Priority**: Medium

#### Tasks:
- [ ] Implement incremental data sync
- [ ] Add data caching in iOS app
- [ ] Optimize database queries
- [ ] Handle FlightAware API rate limits
- [ ] Add data refresh scheduling
- [ ] Implement offline support in iOS app

### Phase 6: Polish & Enhancement ⏳
**Status**: Not Started
**Priority**: Low

#### Tasks:
- [ ] Improve UI/UX design
- [ ] Add data export functionality
- [ ] Create detailed flight analytics
- [ ] Add charts and visualizations
- [ ] Implement push notifications for new flights
- [ ] Add support for multiple aircraft

## Implementation Reference Code

### iOS SwiftUI Application Structure

The conceptual iOS implementation includes the following key components:

#### Data Models
- **Flight**: Represents individual flight records with properties:
  - id (FlightAware ID)
  - tailNumber
  - departureAirport/arrivalAirport
  - departureTime/arrivalTime
  - flightDurationMinutes
  - estimatedRevenue

- **Summary**: Aggregated statistics for a period:
  - period (Daily/Weekly/Monthly/Custom)
  - startDate/endDate
  - totalFlightHours
  - totalRevenue/totalFixedCosts/totalVariableCosts
  - netProfit

#### BackendService Class
- Manages all API communication with the M2 backend
- Implements async/await pattern for modern Swift concurrency
- Provides methods for:
  - `fetchFlights()`: Retrieve flight list
  - `fetchSummary()`: Get aggregated statistics
  - `refreshBackendData()`: Trigger FlightAware sync
- Comprehensive error handling with custom APIError enum

#### Main Views
- **ContentView**: Primary dashboard interface
  - Date range selection with DatePicker
  - Action buttons for data fetching and backend refresh
  - Summary statistics display
  - Flight list with individual flight details
  - Loading states and error messaging
  
- **SettingsView**: Configuration interface
  - Tail number input
  - Financial parameters (revenue/hour, fixed costs, variable costs)
  - Accessible via gear icon in navigation bar

#### Key Implementation Details
- Uses `@StateObject` for BackendService lifecycle management
- ISO 8601 date formatting for backend compatibility
- Proper error localization for user-friendly messages
- SwiftUI sheet presentation for settings
- Number formatting for financial values
- Conditional coloring (green/red) for profit display

## Key Technical Decisions

### Backend Design Choices:
1. **Flask over FastAPI**: Simpler for basic REST API needs
2. **SQLite over PostgreSQL**: No need for complex database features
3. **Local storage**: All data stored on M2, no cloud dependencies
4. **Financial parameters**: Initially hardcoded, later configurable

### iOS Design Choices:
1. **SwiftUI**: Modern, declarative UI framework
2. **URLSession**: Native networking, no third-party dependencies
3. **Local settings storage**: UserDefaults or SwiftData
4. **No authentication**: Personal use only via Tailscale

## Risk Mitigation

### Technical Risks:
1. **FlightAware API changes**: Abstract API calls in separate module
2. **Tailscale connectivity issues**: Add connection status monitoring
3. **Data inconsistency**: Implement transaction logging

### Development Risks:
1. **Scope creep**: Focus on MVP features first
2. **Complex financial calculations**: Start simple, iterate

## Next Steps

1. **Immediate Action**: Set up Python development environment
2. **First Milestone**: Working backend API with test data
3. **Second Milestone**: Basic iOS app displaying flight data
4. **MVP Target**: End-to-end working system with core features

## Success Metrics

- [ ] Backend successfully fetches flight data from FlightAware
- [ ] iOS app displays flight list and summaries
- [ ] Financial calculations match manual calculations
- [ ] System works reliably over Tailscale connection
- [ ] Data persists between sessions

## Notes

- Initial focus on single aircraft (N593EH)
- All times stored in UTC
- Financial parameters can be adjusted per deployment
- No user authentication needed (Tailscale provides security)

## Required Environment Setup

### Backend Prerequisites
- Python 3.8+
- pip package manager
- FlightAware AeroAPI key
- `.env` file with: `FLIGHTAWARE_API_KEY=your_api_key_here`

### iOS Prerequisites  
- Xcode 14.0+
- iOS 16.0+ deployment target
- Swift 5.7+
- Active Apple Developer account (for device testing)

### Connectivity Prerequisites
- Tailscale account
- Tailscale installed on both M2 Mac and iOS device
- Devices connected to same Tailscale network

---
*Last Updated: 2025-07-26*
*Status Legend: ✅ Complete | ⏳ Pending | 🚧 In Progress | ❌ Blocked*