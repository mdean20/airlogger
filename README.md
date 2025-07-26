# AirLogger

Personal aircraft tracking and flight time logging application for N593EH.

## Project Status

✅ **Phase 1 Complete**: Python Flask backend with TDD approach
- Full test coverage (86%)
- FlightAware API integration
- SQLite database with financial tracking
- RESTful API endpoints

⏳ **Phase 2 Pending**: iOS SwiftUI application

## Quick Start

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Copy `.env.example` to `.env` and add your FlightAware API key

3. Run the backend:
   ```bash
   ./run.sh
   ```

The backend will be available at `http://localhost:5000`

## Architecture

- **Backend**: Python Flask API on M2 Mac Mini
- **Frontend**: iOS SwiftUI application (coming soon)
- **Database**: SQLite
- **Connectivity**: Tailscale VPN
- **Data Source**: FlightAware AeroAPI

## Documentation

- [Development Roadmap](ROADMAP.md)
- [Implementation Notes](CLAUDE.md)
- [Backend Documentation](backend/README.md)
