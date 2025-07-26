"""
Tests for AirLogger API endpoints.
"""
import pytest
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock


class TestRefreshDataEndpoint:
    """Test cases for /api/refresh_data endpoint."""
    
    def test_refresh_data_success(self, client, sample_flight_data):
        """Test successful data refresh."""
        with patch('app.api.FlightAwareClient') as mock_client_class:
            # Mock the FlightAware client
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.fetch_aircraft_history.return_value = sample_flight_data["flights"]
            mock_client.process_flight_data.return_value = []
            
            # Make request
            response = client.post('/api/refresh_data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "message" in data
            assert "success" in data["message"].lower()
            
            # Verify FlightAware was called with correct parameters
            mock_client.fetch_aircraft_history.assert_called_once()
            call_args = mock_client.fetch_aircraft_history.call_args[0]
            assert call_args[0] == "N593EH"
            # Should fetch last 90 days
            assert (datetime.now(timezone.utc) - call_args[1]).days >= 89
    
    def test_refresh_data_no_new_flights(self, client):
        """Test refresh when no new flights are found."""
        with patch('app.api.FlightAwareClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_client.fetch_aircraft_history.return_value = []
            
            response = client.post('/api/refresh_data')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "no new data" in data["message"].lower()
    
    def test_refresh_data_api_error(self, client):
        """Test handling of API errors during refresh."""
        with patch('app.api.FlightAwareClient') as mock_client_class:
            mock_client_class.side_effect = ValueError("FLIGHTAWARE_API_KEY not configured")
            
            response = client.post('/api/refresh_data')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert "error" in data
            assert "api configuration" in data["error"].lower()


class TestFlightsEndpoint:
    """Test cases for /api/flights endpoint."""
    
    def test_get_flights_success(self, client, test_db):
        """Test successful retrieval of flights."""
        from app.models import FlightRecord
        
        # Add test flights to database
        flight1 = FlightRecord(
            id="TEST-001",
            tail_number="N593EH",
            departure_airport="KSFO",
            arrival_airport="KLAX",
            departure_time_utc=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 15, 45, tzinfo=timezone.utc),
            flight_duration_minutes=75
        )
        flight2 = FlightRecord(
            id="TEST-002",
            tail_number="N593EH",
            departure_airport="KLAX",
            arrival_airport="KPHX",
            departure_time_utc=datetime(2024, 1, 15, 17, 0, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 18, 30, tzinfo=timezone.utc),
            flight_duration_minutes=90
        )
        
        # Mock database session
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add_all([flight1, flight2])
            test_db.commit()
            
            # Request flights for specific date
            response = client.get('/api/flights?start_date=2024-01-15&end_date=2024-01-15')
            
            assert response.status_code == 200
            flights = json.loads(response.data)
            assert len(flights) == 2
            assert flights[0]["id"] == "TEST-001"
            assert flights[0]["estimatedRevenue"] == 187.50  # 1.25 hours * $150
            assert flights[1]["id"] == "TEST-002"
            assert flights[1]["estimatedRevenue"] == 225.00  # 1.5 hours * $150
    
    def test_get_flights_with_tail_number(self, client, test_db):
        """Test filtering flights by tail number."""
        from app.models import FlightRecord
        
        # Add flights for different tail numbers
        flight1 = FlightRecord(
            id="TEST-003",
            tail_number="N593EH",
            departure_airport="KSFO",
            arrival_airport="KLAX",
            departure_time_utc=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 15, 45, tzinfo=timezone.utc),
            flight_duration_minutes=75
        )
        flight2 = FlightRecord(
            id="TEST-004",
            tail_number="N123AB",  # Different tail number
            departure_airport="KLAX",
            arrival_airport="KPHX",
            departure_time_utc=datetime(2024, 1, 15, 17, 0, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 18, 30, tzinfo=timezone.utc),
            flight_duration_minutes=90
        )
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add_all([flight1, flight2])
            test_db.commit()
            
            # Request flights for specific tail number
            response = client.get('/api/flights?tail_number=N593EH&start_date=2024-01-15&end_date=2024-01-15')
            
            assert response.status_code == 200
            flights = json.loads(response.data)
            assert len(flights) == 1
            assert flights[0]["tailNumber"] == "N593EH"
    
    def test_get_flights_missing_dates(self, client):
        """Test error when dates are missing."""
        response = client.get('/api/flights')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "required" in data["error"]
    
    def test_get_flights_invalid_date_format(self, client):
        """Test error with invalid date format."""
        response = client.get('/api/flights?start_date=15-01-2024&end_date=2024-01-15')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "invalid date format" in data["error"].lower()


class TestSummaryEndpoint:
    """Test cases for /api/summary endpoint."""
    
    def test_get_summary_success(self, client, test_db):
        """Test successful summary calculation."""
        from app.models import FlightRecord, FinancialSettings
        
        # Add financial settings
        settings = FinancialSettings(
            revenue_per_hour=150.0,
            monthly_fixed_costs=500.0,
            variable_cost_per_hour=75.0
        )
        
        # Add test flights
        flights = [
            FlightRecord(
                id="SUM-001",
                tail_number="N593EH",
                departure_airport="KSFO",
                arrival_airport="KLAX",
                departure_time_utc=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
                arrival_time_utc=datetime(2024, 1, 15, 15, 30, tzinfo=timezone.utc),
                flight_duration_minutes=60
            ),
            FlightRecord(
                id="SUM-002",
                tail_number="N593EH",
                departure_airport="KLAX",
                arrival_airport="KPHX",
                departure_time_utc=datetime(2024, 1, 15, 17, 0, tzinfo=timezone.utc),
                arrival_time_utc=datetime(2024, 1, 15, 19, 0, tzinfo=timezone.utc),
                flight_duration_minutes=120
            )
        ]
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add(settings)
            test_db.add_all(flights)
            test_db.commit()
            
            # Request summary
            response = client.get('/api/summary?start_date=2024-01-15&end_date=2024-01-15')
            
            assert response.status_code == 200
            summary = json.loads(response.data)
            
            # Verify calculations
            assert summary["totalFlightHours"] == 3.0  # 60 + 120 minutes = 3 hours
            assert summary["totalRevenue"] == 450.0  # 3 hours * $150
            assert summary["totalVariableCosts"] == 225.0  # 3 hours * $75
            # Fixed costs for 1 day: $500/30.44 ≈ $16.43
            assert 16.0 <= summary["totalFixedCosts"] <= 17.0
            assert summary["netProfit"] == summary["totalRevenue"] - summary["totalVariableCosts"] - summary["totalFixedCosts"]
    
    def test_get_summary_no_flights(self, client, test_db):
        """Test summary when no flights exist."""
        from app.models import FinancialSettings
        
        settings = FinancialSettings(
            revenue_per_hour=150.0,
            monthly_fixed_costs=500.0,
            variable_cost_per_hour=75.0
        )
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add(settings)
            test_db.commit()
            
            response = client.get('/api/summary?start_date=2024-01-15&end_date=2024-01-15')
            
            assert response.status_code == 200
            summary = json.loads(response.data)
            
            assert summary["totalFlightHours"] == 0.0
            assert summary["totalRevenue"] == 0.0
            assert summary["totalVariableCosts"] == 0.0
            # Fixed costs still apply
            assert summary["totalFixedCosts"] > 0
            assert summary["netProfit"] < 0  # Negative due to fixed costs
    
    def test_get_summary_date_range(self, client, test_db):
        """Test summary with multi-day date range."""
        from app.models import FlightRecord, FinancialSettings
        
        settings = FinancialSettings(
            revenue_per_hour=150.0,
            monthly_fixed_costs=500.0,
            variable_cost_per_hour=75.0
        )
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add(settings)
            test_db.commit()
            
            # Request 7-day summary
            response = client.get('/api/summary?start_date=2024-01-15&end_date=2024-01-21')
            
            assert response.status_code == 200
            summary = json.loads(response.data)
            
            # Fixed costs for 7 days
            expected_fixed = (500.0 / 30.44) * 7
            assert abs(summary["totalFixedCosts"] - expected_fixed) < 1.0


class TestFinancialSettingsEndpoints:
    """Test cases for financial settings endpoints."""
    
    def test_get_financial_settings(self, client, test_db):
        """Test retrieving financial settings."""
        from app.models import FinancialSettings
        
        settings = FinancialSettings(
            revenue_per_hour=175.0,
            monthly_fixed_costs=600.0,
            variable_cost_per_hour=80.0
        )
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add(settings)
            test_db.commit()
            
            response = client.get('/api/financial-settings')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["revenue_per_hour"] == 175.0
            assert data["monthly_fixed_costs"] == 600.0
            assert data["variable_cost_per_hour"] == 80.0
    
    def test_update_financial_settings(self, client, test_db):
        """Test updating financial settings."""
        from app.models import FinancialSettings
        
        # Create initial settings
        settings = FinancialSettings(
            revenue_per_hour=150.0,
            monthly_fixed_costs=500.0,
            variable_cost_per_hour=75.0
        )
        
        with patch('app.api.get_db_session') as mock_get_session:
            mock_get_session.return_value = test_db
            test_db.add(settings)
            test_db.commit()
            
            # Update settings
            new_data = {
                "revenue_per_hour": 200.0,
                "monthly_fixed_costs": 700.0,
                "variable_cost_per_hour": 90.0
            }
            
            response = client.put(
                '/api/financial-settings',
                data=json.dumps(new_data),
                content_type='application/json'
            )
            
            assert response.status_code == 200
            updated = json.loads(response.data)
            assert updated["revenue_per_hour"] == 200.0
            assert updated["monthly_fixed_costs"] == 700.0
            assert updated["variable_cost_per_hour"] == 90.0
    
    def test_update_financial_settings_invalid_data(self, client):
        """Test updating with invalid data."""
        invalid_data = {
            "revenue_per_hour": "not a number",
            "monthly_fixed_costs": 500.0,
            "variable_cost_per_hour": 75.0
        }
        
        response = client.put(
            '/api/financial-settings',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data