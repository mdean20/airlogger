"""
Database models for AirLogger.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class FlightRecord(Base):
    """Model for storing individual flight records."""
    __tablename__ = 'flights'
    
    id = Column(String, primary_key=True)  # FlightAware flight ID
    tail_number = Column(String, nullable=False, index=True)
    departure_airport = Column(String, nullable=False)
    arrival_airport = Column(String, nullable=False)
    departure_time_utc = Column(DateTime(timezone=True), nullable=False, index=True)
    arrival_time_utc = Column(DateTime(timezone=True), nullable=False)
    flight_duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self, revenue_per_hour=150.0):
        """Convert FlightRecord to dictionary for JSON response."""
        # Add 15 minutes for ground engine time (Hobbs)
        hobbs_minutes = self.flight_duration_minutes + 15
        
        # Calculate hours and round up to nearest 0.1 hour (6 minutes)
        hobbs_hours = hobbs_minutes / 60.0
        # Round up to nearest 0.1 hour
        billable_hours = round(hobbs_hours * 10 + 0.49) / 10  # Add 0.49 to round up
        
        estimated_revenue = round(billable_hours * revenue_per_hour, 2)
        
        return {
            "id": self.id,
            "tailNumber": self.tail_number,
            "departureAirport": self.departure_airport,
            "arrivalAirport": self.arrival_airport,
            "departureTime": self.departure_time_utc.isoformat(),
            "arrivalTime": self.arrival_time_utc.isoformat(),
            "flightDurationMinutes": self.flight_duration_minutes,
            "hobbsMinutes": hobbs_minutes,
            "billableHours": billable_hours,
            "estimatedRevenue": estimated_revenue
        }


class FinancialSettings(Base):
    """Model for storing financial calculation parameters."""
    __tablename__ = 'financial_settings'
    
    id = Column(Integer, primary_key=True)
    revenue_per_hour = Column(Float, nullable=False)
    monthly_fixed_costs = Column(Float, nullable=False)
    variable_cost_per_hour = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert FinancialSettings to dictionary."""
        return {
            "id": self.id,
            "revenue_per_hour": self.revenue_per_hour,
            "monthly_fixed_costs": self.monthly_fixed_costs,
            "variable_cost_per_hour": self.variable_cost_per_hour,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_or_create_default(cls, session):
        """Get existing settings or create default ones."""
        settings = session.query(cls).first()
        if not settings:
            settings = cls(
                revenue_per_hour=150.0,
                monthly_fixed_costs=500.0,
                variable_cost_per_hour=75.0
            )
            session.add(settings)
            session.commit()
        return settings