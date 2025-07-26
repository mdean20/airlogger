"""
Tests for FlightAware API integration.
"""
import pytest
from datetime import datetime, timezone, timedelta
import requests_mock
import requests


class TestFlightAwareClient:
    """Test cases for FlightAware API client."""
    
    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Mock the API key environment variable."""
        monkeypatch.setenv("FLIGHTAWARE_API_KEY", "test_api_key_123")
    
    def test_fetch_aircraft_history_success(self, mock_api_key, sample_flight_data):
        """Test successful fetch of aircraft history."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        with requests_mock.Mocker() as m:
            # Mock the API response
            m.get(
                "https://aeroapi.flightaware.com/aeroapi/history/aircraft/N593EH",
                json=sample_flight_data,
                status_code=200
            )
            
            # Fetch data
            result = client.fetch_aircraft_history(
                "N593EH",
                datetime.now(timezone.utc) - timedelta(days=90),
                datetime.now(timezone.utc)
            )
            
            # Verify result
            assert result == sample_flight_data["flights"]
            assert len(result) == 2
            
            # Verify request headers
            assert m.last_request.headers["x-apikey"] == "test_api_key_123"
    
    def test_fetch_aircraft_history_no_api_key(self, monkeypatch):
        """Test error when API key is missing."""
        from app.services.flightaware import FlightAwareClient
        
        # Remove API key
        monkeypatch.delenv("FLIGHTAWARE_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="FLIGHTAWARE_API_KEY not configured"):
            client = FlightAwareClient()
    
    def test_fetch_aircraft_history_api_error(self, mock_api_key):
        """Test handling of API errors."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        with requests_mock.Mocker() as m:
            # Mock API error response
            m.get(
                "https://aeroapi.flightaware.com/aeroapi/history/aircraft/N593EH",
                status_code=401,
                json={"error": "Unauthorized"}
            )
            
            # Should return empty list on error
            result = client.fetch_aircraft_history(
                "N593EH",
                datetime.now(timezone.utc) - timedelta(days=90),
                datetime.now(timezone.utc)
            )
            
            assert result == []
    
    def test_fetch_aircraft_history_network_error(self, mock_api_key):
        """Test handling of network errors."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        with requests_mock.Mocker() as m:
            # Mock network error
            m.get(
                "https://aeroapi.flightaware.com/aeroapi/history/aircraft/N593EH",
                exc=requests.exceptions.ConnectionError
            )
            
            # Should return empty list on network error
            result = client.fetch_aircraft_history(
                "N593EH",
                datetime.now(timezone.utc) - timedelta(days=90),
                datetime.now(timezone.utc)
            )
            
            assert result == []
    
    def test_process_flight_data(self, mock_api_key, sample_flight_data):
        """Test processing of raw flight data."""
        from app.services.flightaware import FlightAwareClient
        from app.models import FlightRecord
        
        client = FlightAwareClient()
        
        # Process the sample data
        flights = client.process_flight_data(sample_flight_data["flights"])
        
        assert len(flights) == 2
        
        # Check first flight
        flight1 = flights[0]
        assert isinstance(flight1, FlightRecord)
        assert flight1.id == "UAL123-1234567890-airline-0123"
        assert flight1.tail_number == "N593EH"
        assert flight1.departure_airport == "KSFO"
        assert flight1.arrival_airport == "KLAX"
        assert flight1.flight_duration_minutes == 75
        
        # Check second flight
        flight2 = flights[1]
        assert flight2.id == "UAL456-1234567891-airline-0456"
        assert flight2.flight_duration_minutes == 90
    
    def test_process_flight_data_missing_actual_times(self, mock_api_key):
        """Test processing when actual times are missing (uses filed times)."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        # Flight data with missing actual times
        data = [{
            "fa_flight_id": "TEST-789",
            "ident": "N593EH",
            "origin": {"code": "KSFO"},
            "destination": {"code": "KLAX"},
            "filed_departure_time": "2024-01-15T14:25:00Z",
            "filed_arrival_time": "2024-01-15T15:40:00Z"
        }]
        
        flights = client.process_flight_data(data)
        
        assert len(flights) == 1
        assert flights[0].flight_duration_minutes == 75
    
    def test_process_flight_data_incomplete_record(self, mock_api_key):
        """Test that incomplete records are skipped."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        # Flight data with missing required fields
        data = [
            {
                "fa_flight_id": "INCOMPLETE-123",
                "ident": "N593EH",
                # Missing origin and destination
                "actual_out": "2024-01-15T14:30:00Z",
                "actual_in": "2024-01-15T15:45:00Z"
            },
            {
                "fa_flight_id": "COMPLETE-456",
                "ident": "N593EH",
                "origin": {"code": "KSFO"},
                "destination": {"code": "KLAX"},
                "actual_out": "2024-01-15T14:30:00Z",
                "actual_in": "2024-01-15T15:45:00Z"
            }
        ]
        
        flights = client.process_flight_data(data)
        
        # Should only process the complete record
        assert len(flights) == 1
        assert flights[0].id == "COMPLETE-456"
    
    def test_process_flight_data_negative_duration(self, mock_api_key):
        """Test handling of negative flight duration."""
        from app.services.flightaware import FlightAwareClient
        
        client = FlightAwareClient()
        
        # Flight with arrival before departure (data error)
        data = [{
            "fa_flight_id": "NEGATIVE-123",
            "ident": "N593EH",
            "origin": {"code": "KSFO"},
            "destination": {"code": "KLAX"},
            "actual_out": "2024-01-15T15:45:00Z",  # Later than arrival
            "actual_in": "2024-01-15T14:30:00Z"
        }]
        
        flights = client.process_flight_data(data)
        
        assert len(flights) == 1
        assert flights[0].flight_duration_minutes == 0  # Should be set to 0, not negative