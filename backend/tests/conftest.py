"""
Pytest configuration and fixtures for AirLogger backend tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os


@pytest.fixture(scope="function")
def test_db():
    """Create a temporary database for testing."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    db_url = f"sqlite:///{db_path}"
    
    # Import here to avoid circular imports
    from app.models import Base
    
    # Create engine and tables
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Cleanup
    session.close()
    engine.dispose()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def app():
    """Create Flask app for testing."""
    from app import create_app
    
    # Create app with testing config
    app = create_app(testing=True)
    
    return app


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def sample_flight_data():
    """Sample flight data matching FlightAware API response."""
    return {
        "flights": [
            {
                "fa_flight_id": "UAL123-1234567890-airline-0123",
                "ident": "N593EH",
                "origin": {
                    "code": "KSFO",
                    "icao": "KSFO"
                },
                "destination": {
                    "code": "KLAX",
                    "icao": "KLAX"
                },
                "actual_out": "2024-01-15T14:30:00Z",
                "actual_in": "2024-01-15T15:45:00Z",
                "filed_departure_time": "2024-01-15T14:25:00Z",
                "filed_arrival_time": "2024-01-15T15:40:00Z"
            },
            {
                "fa_flight_id": "UAL456-1234567891-airline-0456",
                "ident": "N593EH",
                "origin": {
                    "code": "KLAX",
                    "icao": "KLAX"
                },
                "destination": {
                    "code": "KPHX",
                    "icao": "KPHX"
                },
                "actual_out": "2024-01-15T17:00:00Z",
                "actual_in": "2024-01-15T18:30:00Z",
                "filed_departure_time": "2024-01-15T16:55:00Z",
                "filed_arrival_time": "2024-01-15T18:25:00Z"
            }
        ]
    }


@pytest.fixture
def sample_financial_settings():
    """Sample financial settings data."""
    return {
        "revenue_per_hour": 150.0,
        "monthly_fixed_costs": 500.0,
        "variable_cost_per_hour": 75.0
    }