# AirLogger Backend

Python Flask backend for the AirLogger aircraft tracking application.

## Setup

1. **Install Python 3.8+**

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your FlightAware API key to `.env`

5. **Run the application**:
   ```bash
   python app.py
   ```

## API Endpoints

- `POST /api/refresh_data` - Fetch latest flight data from FlightAware
- `GET /api/flights` - Get flight records for a date range
- `GET /api/summary` - Get financial summary for a date range
- `GET /api/financial-settings` - Get current financial parameters
- `PUT /api/financial-settings` - Update financial parameters

## Testing

Run tests with coverage:
```bash
pytest
```

## Database

The application uses SQLite with the database file `airlogger.db` created automatically on first run.

## Tailscale Setup

1. Install Tailscale on your M2 Mac
2. Note your machine's Tailscale IP address
3. The backend runs on `0.0.0.0:5000` to be accessible via Tailscale

## Environment Variables

- `FLIGHTAWARE_API_KEY` - Your FlightAware AeroAPI key (required)
- `FLASK_PORT` - Port to run the server on (default: 5000)
- `FLASK_ENV` - Environment mode (development/production)