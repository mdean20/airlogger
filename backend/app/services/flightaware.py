"""
FlightAware API integration service.
"""
import os
import requests
from datetime import datetime, timezone
import logging
from typing import List, Dict, Any
from app.models import FlightRecord

logger = logging.getLogger(__name__)


class FlightAwareClient:
    """Client for interacting with FlightAware AeroAPI."""
    
    def __init__(self):
        """Initialize FlightAware client."""
        self.api_key = os.getenv("FLIGHTAWARE_API_KEY")
        if not self.api_key:
            raise ValueError("FLIGHTAWARE_API_KEY not configured")
        
        self.base_url = "https://aeroapi.flightaware.com/aeroapi"
        self.headers = {"x-apikey": self.api_key}
    
    def fetch_aircraft_history(self, registration: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch historical flight data for an aircraft.
        
        Args:
            registration: Aircraft registration (e.g., "N593EH")
            start_date: Start date for history query
            end_date: End date for history query
            
        Returns:
            List of flight dictionaries from FlightAware
        """
        try:
            # Use the flights endpoint which works for tail numbers
            url = f"{self.base_url}/flights/{registration}"
            logger.info(f"Fetching flights for {registration}")
            
            # The flights endpoint returns recent flights, we'll filter by date after
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            all_flights = data.get("flights", [])
            
            # Filter flights by date range
            filtered_flights = []
            for flight in all_flights:
                # Get departure time
                dep_time_str = (
                    flight.get("actual_off") or 
                    flight.get("actual_out") or 
                    flight.get("scheduled_off") or
                    flight.get("filed_departure_time")
                )
                
                if dep_time_str:
                    try:
                        dep_time = self._parse_datetime(dep_time_str)
                        if start_date <= dep_time <= end_date:
                            filtered_flights.append(flight)
                    except Exception as e:
                        logger.warning(f"Could not parse date for flight: {e}")
            
            logger.info(f"Retrieved {len(all_flights)} total flights, {len(filtered_flights)} within date range")
            return filtered_flights
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from FlightAware: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in fetch_aircraft_history: {e}")
            return []
    
    def process_flight_data(self, raw_flights: List[Dict[str, Any]]) -> List[FlightRecord]:
        """
        Process raw flight data from FlightAware into FlightRecord objects.
        
        Args:
            raw_flights: List of raw flight dictionaries from FlightAware
            
        Returns:
            List of FlightRecord objects
        """
        processed_flights = []
        
        for flight_data in raw_flights:
            try:
                # Extract required fields
                flight_id = flight_data.get("fa_flight_id")
                tail_number = flight_data.get("ident")
                
                # Get airport codes
                origin = flight_data.get("origin", {})
                destination = flight_data.get("destination", {})
                departure_airport = origin.get("icao") or origin.get("code")
                arrival_airport = destination.get("icao") or destination.get("code")
                
                # Skip cancelled flights
                if flight_data.get("cancelled", False):
                    logger.info(f"Skipping cancelled flight: {flight_id}")
                    continue
                
                # Get times - try multiple field names
                departure_time_str = (
                    flight_data.get("actual_off") or
                    flight_data.get("actual_out") or 
                    flight_data.get("scheduled_off") or
                    flight_data.get("scheduled_out") or
                    flight_data.get("filed_departure_time")
                )
                arrival_time_str = (
                    flight_data.get("actual_on") or
                    flight_data.get("actual_in") or 
                    flight_data.get("scheduled_on") or
                    flight_data.get("scheduled_in") or
                    flight_data.get("filed_arrival_time")
                )
                
                # Validate required fields
                if not all([flight_id, tail_number, departure_airport, arrival_airport, 
                           departure_time_str, arrival_time_str]):
                    logger.warning(f"Skipping incomplete flight record: {flight_id or 'Unknown'}")
                    continue
                
                # Parse times
                departure_time = self._parse_datetime(departure_time_str)
                arrival_time = self._parse_datetime(arrival_time_str)
                
                # Calculate duration
                duration = arrival_time - departure_time
                flight_duration_minutes = int(duration.total_seconds() / 60)
                
                # Handle negative durations
                if flight_duration_minutes < 0:
                    logger.warning(f"Negative duration for flight {flight_id}, setting to 0")
                    flight_duration_minutes = 0
                
                # Create FlightRecord
                flight_record = FlightRecord(
                    id=flight_id,
                    tail_number=tail_number,
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    departure_time_utc=departure_time,
                    arrival_time_utc=arrival_time,
                    flight_duration_minutes=flight_duration_minutes
                )
                
                processed_flights.append(flight_record)
                
            except Exception as e:
                logger.error(f"Error processing flight {flight_data.get('fa_flight_id', 'Unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_flights)} flights successfully")
        return processed_flights
    
    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string from FlightAware (ISO 8601 format)."""
        # Handle 'Z' suffix for UTC
        if datetime_str.endswith('Z'):
            datetime_str = datetime_str[:-1] + '+00:00'
        
        # Parse ISO format
        dt = datetime.fromisoformat(datetime_str)
        
        # Ensure timezone aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        return dt