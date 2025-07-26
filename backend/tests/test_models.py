"""
Tests for AirLogger database models.
"""
import pytest
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError


class TestFlightRecord:
    """Test cases for FlightRecord model."""
    
    def test_create_flight_record(self, test_db):
        """Test creating a basic flight record."""
        from app.models import FlightRecord
        
        flight = FlightRecord(
            id="TEST-123",
            tail_number="N593EH",
            departure_airport="KSFO",
            arrival_airport="KLAX",
            departure_time_utc=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 15, 45, tzinfo=timezone.utc),
            flight_duration_minutes=75
        )
        
        test_db.add(flight)
        test_db.commit()
        
        # Verify the flight was saved
        saved_flight = test_db.query(FlightRecord).filter_by(id="TEST-123").first()
        assert saved_flight is not None
        assert saved_flight.tail_number == "N593EH"
        assert saved_flight.departure_airport == "KSFO"
        assert saved_flight.arrival_airport == "KLAX"
        assert saved_flight.flight_duration_minutes == 75
    
    def test_flight_record_to_dict(self, test_db):
        """Test converting FlightRecord to dictionary."""
        from app.models import FlightRecord
        
        flight = FlightRecord(
            id="TEST-456",
            tail_number="N593EH",
            departure_airport="KLAX",
            arrival_airport="KPHX",
            departure_time_utc=datetime(2024, 1, 15, 17, 0, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 18, 30, tzinfo=timezone.utc),
            flight_duration_minutes=90
        )
        
        flight_dict = flight.to_dict()
        
        assert flight_dict["id"] == "TEST-456"
        assert flight_dict["tailNumber"] == "N593EH"
        assert flight_dict["departureAirport"] == "KLAX"
        assert flight_dict["arrivalAirport"] == "KPHX"
        assert flight_dict["flightDurationMinutes"] == 90
        assert "departureTime" in flight_dict
        assert "arrivalTime" in flight_dict
        assert "estimatedRevenue" in flight_dict
    
    def test_duplicate_flight_id_rejected(self, test_db):
        """Test that duplicate flight IDs are rejected."""
        from app.models import FlightRecord
        
        # Create first flight
        flight1 = FlightRecord(
            id="DUPLICATE-123",
            tail_number="N593EH",
            departure_airport="KSFO",
            arrival_airport="KLAX",
            departure_time_utc=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 15, 45, tzinfo=timezone.utc),
            flight_duration_minutes=75
        )
        test_db.add(flight1)
        test_db.commit()
        
        # Try to create duplicate
        flight2 = FlightRecord(
            id="DUPLICATE-123",  # Same ID
            tail_number="N593EH",
            departure_airport="KLAX",
            arrival_airport="KPHX",
            departure_time_utc=datetime(2024, 1, 15, 17, 0, tzinfo=timezone.utc),
            arrival_time_utc=datetime(2024, 1, 15, 18, 30, tzinfo=timezone.utc),
            flight_duration_minutes=90
        )
        test_db.add(flight2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestFinancialSettings:
    """Test cases for FinancialSettings model."""
    
    def test_create_financial_settings(self, test_db):
        """Test creating financial settings."""
        from app.models import FinancialSettings
        
        settings = FinancialSettings(
            revenue_per_hour=150.0,
            monthly_fixed_costs=500.0,
            variable_cost_per_hour=75.0
        )
        
        test_db.add(settings)
        test_db.commit()
        
        # Verify settings were saved
        saved_settings = test_db.query(FinancialSettings).first()
        assert saved_settings is not None
        assert saved_settings.revenue_per_hour == 150.0
        assert saved_settings.monthly_fixed_costs == 500.0
        assert saved_settings.variable_cost_per_hour == 75.0
    
    def test_financial_settings_to_dict(self, test_db):
        """Test converting FinancialSettings to dictionary."""
        from app.models import FinancialSettings
        
        settings = FinancialSettings(
            revenue_per_hour=175.0,
            monthly_fixed_costs=600.0,
            variable_cost_per_hour=80.0
        )
        
        settings_dict = settings.to_dict()
        
        assert settings_dict["revenue_per_hour"] == 175.0
        assert settings_dict["monthly_fixed_costs"] == 600.0
        assert settings_dict["variable_cost_per_hour"] == 80.0
        assert "id" in settings_dict
        assert "updated_at" in settings_dict
    
    def test_get_or_create_default(self, test_db):
        """Test get_or_create_default method."""
        from app.models import FinancialSettings
        
        # First call should create default settings
        settings1 = FinancialSettings.get_or_create_default(test_db)
        assert settings1.revenue_per_hour == 150.0
        assert settings1.monthly_fixed_costs == 500.0
        assert settings1.variable_cost_per_hour == 75.0
        
        # Second call should return the same settings
        settings2 = FinancialSettings.get_or_create_default(test_db)
        assert settings2.id == settings1.id
        assert test_db.query(FinancialSettings).count() == 1